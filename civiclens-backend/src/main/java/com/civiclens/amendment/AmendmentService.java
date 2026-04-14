package com.civiclens.amendment;

import com.civiclens.amendment.dto.*;
import com.civiclens.analytics.AmendmentAnalytics;
import com.civiclens.analytics.AnalyticsRepository;
import com.civiclens.analytics.AnalyticsSyncService;
import com.civiclens.comment.CommentRepository;
import com.civiclens.common.dto.PagedResponse;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.user.*;
import com.civiclens.vote.VoteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.*;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class AmendmentService {

    private final AmendmentRepository amendmentRepository;
    private final UserRepository userRepository;
    private final VoteRepository voteRepository;
    private final CommentRepository commentRepository;
    private final AnalyticsRepository analyticsRepository;
    private final AnalyticsSyncService analyticsSyncService;

    @Transactional
    public AmendmentResponse create(AmendmentRequest request, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Amendment amendment = Amendment.builder()
                .title(request.getTitle())
                .body(request.getBody())
                .category(request.getCategory())
                .closesAt(request.getClosesAt())
                .createdBy(user)
                .build();

        amendment = amendmentRepository.save(amendment);

        // Initialize empty analytics row
        AmendmentAnalytics analytics = AmendmentAnalytics.builder()
                .amendment(amendment)
                .build();
        analyticsRepository.save(analytics);
        queueAnalyticsRefreshAfterCommit(amendment.getId(), false, "amendment-created");

        log.info("Amendment created: id={}, title={}", amendment.getId(), amendment.getTitle());
        return toResponse(amendment);
    }

    public PagedResponse<AmendmentResponse> list(String sort, String category, String status, int page, int size) {
        Sort sorting = switch (sort != null ? sort : "LATEST") {
            case "MOST_UPVOTED" -> Sort.by(Sort.Direction.DESC, "id"); // we'll sort in-memory or via query
            case "MOST_NEGATIVE" -> Sort.by(Sort.Direction.ASC, "id");
            default -> Sort.by(Sort.Direction.DESC, "createdAt");
        };

        Pageable pageable = PageRequest.of(page, size, sorting);
        Page<Amendment> amendments;

        AmendmentStatus statusEnum = null;
        if (status != null && !status.isEmpty()) {
            try {
                statusEnum = AmendmentStatus.valueOf(status);
            } catch (IllegalArgumentException ignored) {
                // Invalid status value — ignore and return all
            }
        }

        if (statusEnum != null && category != null && !category.isEmpty()) {
            AmendmentCategory cat = AmendmentCategory.valueOf(category);
            amendments = amendmentRepository.findByStatusAndCategory(statusEnum, cat, pageable);
        } else if (statusEnum != null) {
            amendments = amendmentRepository.findByStatus(statusEnum, pageable);
        } else if (category != null && !category.isEmpty()) {
            AmendmentCategory cat = AmendmentCategory.valueOf(category);
            amendments = amendmentRepository.findByCategory(cat, pageable);
        } else {
            amendments = amendmentRepository.findAll(pageable);
        }

        List<AmendmentResponse> content = amendments.getContent().stream()
                .map(this::toResponse)
                .collect(Collectors.toList());

        // Sort by votes if requested
        if ("MOST_UPVOTED".equals(sort)) {
            content.sort((a, b) -> (b.getUpvotes() - b.getDownvotes()) - (a.getUpvotes() - a.getDownvotes()));
        } else if ("MOST_NEGATIVE".equals(sort)) {
            content.sort((a, b) -> {
                Double sentA = a.getSentimentMean() != null ? a.getSentimentMean() : 0;
                Double sentB = b.getSentimentMean() != null ? b.getSentimentMean() : 0;
                return Double.compare(sentA, sentB);
            });
        }

        return PagedResponse.<AmendmentResponse>builder()
                .content(content)
                .page(amendments.getNumber())
                .size(amendments.getSize())
                .totalElements(amendments.getTotalElements())
                .totalPages(amendments.getTotalPages())
                .last(amendments.isLast())
                .build();
    }

    public AmendmentResponse getById(Long id) {
        Amendment amendment = amendmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found: " + id));
        return toResponse(amendment);
    }

    @Transactional
    public AmendmentResponse update(Long id, AmendmentRequest request) {
        Amendment amendment = amendmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found: " + id));

        amendment.setTitle(request.getTitle());
        amendment.setBody(request.getBody());
        amendment.setCategory(request.getCategory());
        if (request.getClosesAt() != null) {
            amendment.setClosesAt(request.getClosesAt());
        }

        amendment = amendmentRepository.save(amendment);
        queueAnalyticsRefreshAfterCommit(amendment.getId(), true, "amendment-updated");
        log.info("Amendment updated: id={}", id);
        return toResponse(amendment);
    }

    /**
     * Close expired amendments every minute.
     */
    @Scheduled(fixedRate = 60000)
    @Transactional
    public void closeExpiredAmendments() {
        List<Amendment> expired = amendmentRepository.findExpiredAmendments();
        for (Amendment a : expired) {
            a.setStatus(AmendmentStatus.CLOSED);
            amendmentRepository.save(a);
            log.info("Amendment auto-closed: id={}", a.getId());
        }
    }

    private AmendmentResponse toResponse(Amendment a) {
        int up = commentRepository.sumUpvotesByAmendmentId(a.getId());
        int down = commentRepository.sumDownvotesByAmendmentId(a.getId());
        int comments = commentRepository.countByAmendmentId(a.getId());

        AmendmentResponse.AmendmentResponseBuilder builder = AmendmentResponse.builder()
                .id(a.getId())
                .title(a.getTitle())
                .body(a.getBody())
                .category(a.getCategory().name())
                .status(a.getStatus().name())
                .createdAt(a.getCreatedAt())
                .closesAt(a.getClosesAt())
                .createdByUsername(a.getCreatedBy().getUsername())
                .upvotes(up)
                .downvotes(down)
                .commentCount(comments);

        // Attach analytics preview
        analyticsRepository.findByAmendmentId(a.getId()).ifPresent(analytics -> {
            builder.sentimentMean(analytics.getSentimentMean());
            builder.controversyScore(analytics.getControversyScore());
            builder.controversyLabel(analytics.getControversyLabel());
        });
        if (analyticsSyncService != null && analyticsSyncService.isRefreshNeeded(a.getId())) {
            analyticsSyncService.requestRefresh(a.getId(), false, "amendment-list-stale");
        }

        return builder.build();
    }

    @Transactional
    public void deleteAmendment(Long id) {
        Amendment amendment = amendmentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found: " + id));

        // Delete analytics
        analyticsRepository.findByAmendmentId(id).ifPresent(analyticsRepository::delete);

        // Delete votes linked to comments on this amendment
        voteRepository.deleteByAmendmentId(id);

        // Delete comments on this amendment
        commentRepository.deleteByAmendmentId(id);

        // Finally, delete the amendment itself
        amendmentRepository.delete(amendment);
        
        log.info("Amendment deleted along with cascade records: id={}", id);
    }

    private void queueAnalyticsRefreshAfterCommit(Long amendmentId, boolean force, String reason) {
        if (analyticsSyncService == null) {
            return;
        }

        if (TransactionSynchronizationManager.isSynchronizationActive()) {
            TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
                @Override
                public void afterCommit() {
                    analyticsSyncService.requestRefresh(amendmentId, force, reason);
                }
            });
            return;
        }

        analyticsSyncService.requestRefresh(amendmentId, force, reason);
    }
}
