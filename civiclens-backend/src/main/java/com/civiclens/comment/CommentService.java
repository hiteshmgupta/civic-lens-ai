package com.civiclens.comment;

import com.civiclens.amendment.*;
import com.civiclens.analytics.AnalyticsSyncService;
import com.civiclens.comment.dto.*;
import com.civiclens.common.dto.PagedResponse;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.user.*;
import com.civiclens.vote.VoteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class CommentService {

    private final CommentRepository commentRepository;
    private final AmendmentRepository amendmentRepository;
    private final UserRepository userRepository;
    private final VoteRepository voteRepository;
    private final AnalyticsSyncService analyticsSyncService;

    @Transactional
    public CommentResponse create(Long amendmentId, CommentRequest request, String userEmail) {
        Amendment amendment = amendmentRepository.findById(amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found"));

        if (amendment.getStatus() == AmendmentStatus.CLOSED) {
            throw new IllegalArgumentException("Cannot comment on a closed amendment");
        }

        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        Comment comment = Comment.builder()
                .amendment(amendment)
                .user(user)
                .body(request.getBody())
                .build();

        comment = commentRepository.save(comment);
        log.info("Comment added: amendment={}, user={}", amendmentId, user.getId());
        queueAnalyticsRefreshAfterCommit(amendmentId, "comment-created");

        return toResponse(comment);
    }

    public PagedResponse<CommentResponse> list(Long amendmentId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<Comment> comments = commentRepository.findByAmendmentId(amendmentId, pageable);

        List<CommentResponse> content = comments.getContent().stream()
                .map(this::toResponse)
                .collect(Collectors.toList());

        return PagedResponse.<CommentResponse>builder()
                .content(content)
                .page(comments.getNumber())
                .size(comments.getSize())
                .totalElements(comments.getTotalElements())
                .totalPages(comments.getTotalPages())
                .last(comments.isLast())
                .build();
    }

    private CommentResponse toResponse(Comment c) {
        return CommentResponse.builder()
                .id(c.getId())
                .body(c.getBody())
                .username(c.getUser().getUsername())
                .upvotes(c.getUpvoteCount())
                .downvotes(c.getDownvoteCount())
                .createdAt(c.getCreatedAt())
                .build();
    }

    private void queueAnalyticsRefreshAfterCommit(Long amendmentId, String reason) {
        if (analyticsSyncService == null) {
            return;
        }

        if (TransactionSynchronizationManager.isSynchronizationActive()) {
            TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
                @Override
                public void afterCommit() {
                    analyticsSyncService.requestRefresh(amendmentId, false, reason);
                }
            });
            return;
        }

        analyticsSyncService.requestRefresh(amendmentId, false, reason);
    }

    @Transactional
    public void deleteComment(Long commentId) {
        Comment comment = commentRepository.findById(commentId)
                .orElseThrow(() -> new ResourceNotFoundException("Comment not found: " + commentId));

        Long amendmentId = comment.getAmendment().getId();

        // Delete votes on this comment first
        voteRepository.deleteByCommentId(commentId);

        // Delete the comment
        commentRepository.delete(comment);
        log.info("Comment deleted: id={}, amendment={}", commentId, amendmentId);

        queueAnalyticsRefreshAfterCommit(amendmentId, "comment-deleted");
    }
}
