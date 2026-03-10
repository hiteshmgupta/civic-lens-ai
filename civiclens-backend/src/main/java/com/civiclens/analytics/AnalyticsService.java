package com.civiclens.analytics;

import com.civiclens.amendment.*;
import com.civiclens.analytics.dto.*;
import com.civiclens.comment.*;
import com.civiclens.common.exception.ResourceNotFoundException;
import com.civiclens.vote.VoteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class AnalyticsService {

    private final AnalyticsRepository analyticsRepository;
    private final AmendmentRepository amendmentRepository;
    private final CommentRepository commentRepository;
    private final VoteRepository voteRepository;
    private final AiServiceClient aiServiceClient;
    private final ControversyCalculator calculator;

    public AnalyticsResponse getAnalytics(Long amendmentId) {
        Optional<AmendmentAnalytics> analytics = analyticsRepository.findByAmendmentId(amendmentId);
        if (analytics.isPresent()) {
            return toResponse(analytics.get());
        }
        // Return default empty analytics so the frontend can show the "Generate Analysis" button
        // instead of the error page when no analysis has been triggered yet
        return AnalyticsResponse.builder()
                .amendmentId(amendmentId)
                .totalComments(0)
                .totalVotes(0)
                .upvotes(0)
                .downvotes(0)
                .controversyScore(0.0)
                .controversyLabel("N/A")
                .build();
    }

    @Transactional
    public AnalyticsResponse triggerAnalysis(Long amendmentId) {
        Amendment amendment = amendmentRepository.findById(amendmentId)
                .orElseThrow(() -> new ResourceNotFoundException("Amendment not found: " + amendmentId));

        List<Comment> comments = commentRepository.findByAmendmentId(amendmentId);
        List<String> commentTexts = comments.stream()
                .map(Comment::getBody)
                .collect(Collectors.toList());

        // Call AI service
        AiAnalysisRequest aiRequest = AiAnalysisRequest.builder()
                .amendmentId(amendmentId)
                .amendmentText(amendment.getBody())
                .comments(commentTexts)
                .build();

        AiAnalysisResponse aiResponse = aiServiceClient.analyze(aiRequest);

        // Calculate controversy index components
        int upvotes = voteRepository.countUpvotes(amendmentId);
        int downvotes = voteRepository.countDownvotes(amendmentId);
        int totalComments = comments.size();
        long maxComments = amendmentRepository.count() > 0 ? commentRepository.count() / amendmentRepository.count()
                : 1;

        double[] sentimentScores = aiResponse.getSentimentScores().stream()
                .mapToDouble(Double::doubleValue).toArray();

        double S = calculator.sentimentVariance(sentimentScores);
        double P = calculator.votePolarity(upvotes, downvotes);
        double D = calculator.stanceEntropy(aiResponse.getStanceCounts());
        double E = calculator.engagementIntensity(totalComments, (int) Math.max(maxComments * 3, 100));
        double C = calculator.controversyScore(S, P, D, E);
        String label = calculator.controversyLabel(C);

        // Persist analytics
        AmendmentAnalytics analytics = analyticsRepository.findByAmendmentId(amendmentId)
                .orElse(AmendmentAnalytics.builder().amendment(amendment).build());

        analytics.setSentimentMean(calculator.sentimentMean(sentimentScores));
        analytics.setSentimentVariance(S);
        analytics.setSentimentDistribution(aiResponse.getSentimentDistribution());
        analytics.setSentimentTimeline(aiResponse.getSentimentTimeline());
        analytics.setTopicClusters(aiResponse.getTopicClusters());
        analytics.setTopSupporting(aiResponse.getTopSupporting());
        analytics.setTopOpposing(aiResponse.getTopOpposing());
        analytics.setTotalComments(totalComments);
        analytics.setTotalVotes(upvotes + downvotes);
        analytics.setUpvotes(upvotes);
        analytics.setDownvotes(downvotes);
        analytics.setVotePolarity(P);
        analytics.setStanceEntropy(D);
        analytics.setEngagementScore(E);
        analytics.setControversyScore(C);
        analytics.setControversyLabel(label);
        analytics.setPolicyBrief(aiResponse.getPolicyBrief());
        analytics.setLastComputedAt(LocalDateTime.now());

        analytics = analyticsRepository.save(analytics);
        log.info("Analytics computed for amendment {}: controversy={}, label={}", amendmentId, C, label);

        return toResponse(analytics);
    }

    private AnalyticsResponse toResponse(AmendmentAnalytics a) {
        return AnalyticsResponse.builder()
                .amendmentId(a.getAmendment().getId())
                .sentimentMean(a.getSentimentMean())
                .sentimentVariance(a.getSentimentVariance())
                .sentimentDistribution(a.getSentimentDistribution())
                .sentimentTimeline(a.getSentimentTimeline())
                .topicClusters(a.getTopicClusters())
                .topSupporting(a.getTopSupporting())
                .topOpposing(a.getTopOpposing())
                .totalComments(a.getTotalComments())
                .totalVotes(a.getTotalVotes())
                .upvotes(a.getUpvotes())
                .downvotes(a.getDownvotes())
                .votePolarity(a.getVotePolarity())
                .stanceEntropy(a.getStanceEntropy())
                .engagementScore(a.getEngagementScore())
                .controversyScore(a.getControversyScore())
                .controversyLabel(a.getControversyLabel())
                .policyBrief(a.getPolicyBrief())
                .build();
    }
}
