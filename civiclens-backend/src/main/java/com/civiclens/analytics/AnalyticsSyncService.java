package com.civiclens.analytics;

import com.civiclens.comment.CommentRepository;
import com.civiclens.vote.VoteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Service
@RequiredArgsConstructor
@Slf4j
public class AnalyticsSyncService {

    private final AnalyticsRepository analyticsRepository;
    private final AnalyticsService analyticsService;
    private final CommentRepository commentRepository;
    private final VoteRepository voteRepository;

    private final Set<Long> inFlightRefreshes = ConcurrentHashMap.newKeySet();

    @Async
    public void requestRefresh(Long amendmentId, boolean force, String reason) {
        if (amendmentId == null) {
            return;
        }

        if (!inFlightRefreshes.add(amendmentId)) {
            log.debug("Analytics refresh already running for amendment {} (reason={})", amendmentId, reason);
            return;
        }

        try {
            if (!force && !isRefreshNeeded(amendmentId)) {
                return;
            }

            analyticsService.triggerAnalysis(amendmentId);
            log.info("Analytics refresh completed for amendment {} (reason={})", amendmentId, reason);
        } catch (Exception e) {
            log.warn("Analytics refresh failed for amendment {} (reason={}): {}", amendmentId, reason, e.getMessage());
        } finally {
            inFlightRefreshes.remove(amendmentId);
        }
    }

    public boolean isRefreshNeeded(Long amendmentId) {
        int totalComments = commentRepository.countByAmendmentId(amendmentId);
        int upvotes = voteRepository.countUpvotesByAmendmentId(amendmentId);
        int downvotes = voteRepository.countDownvotesByAmendmentId(amendmentId);
        int totalVotes = upvotes + downvotes;

        Optional<AmendmentAnalytics> analyticsOpt = analyticsRepository.findByAmendmentId(amendmentId);
        if (analyticsOpt.isEmpty()) {
            return totalComments > 0 || totalVotes > 0;
        }

        AmendmentAnalytics analytics = analyticsOpt.get();
        if (analytics.getLastComputedAt() == null) {
            return totalComments > 0 || totalVotes > 0;
        }

        if (!Objects.equals(analytics.getTotalComments(), totalComments)) {
            return true;
        }
        if (!Objects.equals(analytics.getTotalVotes(), totalVotes)) {
            return true;
        }

        String policyBrief = analytics.getPolicyBrief();
        if (totalComments > 0 && (policyBrief == null || policyBrief.isBlank())) {
            return true;
        }
        return totalComments > 0 && containsFailureMarker(policyBrief);
    }

    private boolean containsFailureMarker(String policyBrief) {
        if (policyBrief == null) {
            return false;
        }

        String normalized = policyBrief.toLowerCase();
        return normalized.contains("generation failed")
                || normalized.contains("insufficient data for analysis");
    }
}

