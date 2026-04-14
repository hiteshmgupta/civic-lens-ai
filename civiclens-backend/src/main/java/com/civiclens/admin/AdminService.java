package com.civiclens.admin;

import com.civiclens.admin.dto.DashboardResponse;
import com.civiclens.amendment.*;
import com.civiclens.analytics.*;
import com.civiclens.comment.CommentRepository;
import com.civiclens.user.UserRepository;
import com.civiclens.vote.VoteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class AdminService {

    private final AmendmentRepository amendmentRepository;
    private final UserRepository userRepository;
    private final CommentRepository commentRepository;
    private final VoteRepository voteRepository;
    private final AnalyticsRepository analyticsRepository;

    public DashboardResponse getDashboard() {
        long totalAmendments = amendmentRepository.count();
        long activeAmendments = amendmentRepository.countByStatus(AmendmentStatus.ACTIVE);
        long closedAmendments = amendmentRepository.countByStatus(AmendmentStatus.CLOSED);
        long totalUsers = userRepository.count();
        long totalComments = commentRepository.count();
        long totalVotes = commentRepository.sumAllUpvotes() + commentRepository.sumAllDownvotes();

        // All analytics records
        List<AmendmentAnalytics> allAnalytics = analyticsRepository.findAll();

        // ─── Global sentiment mean ───
        double globalSentiment = allAnalytics.stream()
                .filter(a -> a.getSentimentMean() != null)
                .mapToDouble(AmendmentAnalytics::getSentimentMean)
                .average().orElse(0.0);

        // ─── Global sentiment distribution (aggregate per-amendment distributions) ───
        Map<String, Long> globalSentimentDistribution = new LinkedHashMap<>();
        globalSentimentDistribution.put("positive", 0L);
        globalSentimentDistribution.put("negative", 0L);
        globalSentimentDistribution.put("neutral", 0L);

        for (AmendmentAnalytics analytics : allAnalytics) {
            Map<String, Integer> dist = analytics.getSentimentDistribution();
            if (dist != null) {
                dist.forEach((key, value) -> {
                    if (value != null) {
                        String normalizedKey = key.toLowerCase().trim();
                        globalSentimentDistribution.merge(normalizedKey, value.longValue(), Long::sum);
                    }
                });
            }
        }

        // ─── Most controversial (top 5) ───
        List<Map<String, Object>> mostControversial = allAnalytics.stream()
                .filter(a -> a.getControversyScore() != null && a.getControversyScore() > 0)
                .sorted((a, b) -> Double.compare(b.getControversyScore(), a.getControversyScore()))
                .limit(5)
                .map(a -> {
                    Map<String, Object> map = new LinkedHashMap<>();
                    map.put("id", a.getAmendment().getId());
                    map.put("title", a.getAmendment().getTitle());
                    map.put("category", a.getAmendment().getCategory() != null
                            ? a.getAmendment().getCategory().name() : "GENERAL");
                    map.put("commentCount", a.getTotalComments() != null ? a.getTotalComments() : 0);
                    map.put("controversyScore", a.getControversyScore());
                    map.put("controversyLabel", a.getControversyLabel());
                    return map;
                })
                .collect(Collectors.toList());

        // ─── Participation trend (comments + votes grouped by month) ───
        Map<String, Long> commentsByMonth = new LinkedHashMap<>();
        try {
            List<Object[]> commentCounts = commentRepository.countGroupedByMonth();
            for (Object[] row : commentCounts) {
                String period = String.valueOf(row[0]);
                Long count = ((Number) row[1]).longValue();
                commentsByMonth.put(period, count);
            }
        } catch (Exception e) {
            log.warn("Failed to query comment participation trend: {}", e.getMessage());
        }

        Map<String, Long> votesByMonth = new LinkedHashMap<>();
        try {
            List<Object[]> voteCounts = commentRepository.sumVotesGroupedByMonth();
            for (Object[] row : voteCounts) {
                String period = String.valueOf(row[0]);
                Long count = ((Number) row[1]).longValue();
                votesByMonth.put(period, count);
            }
        } catch (Exception e) {
            log.warn("Failed to query vote participation trend: {}", e.getMessage());
        }

        // Merge all periods into a unified sorted list
        Set<String> allPeriods = new TreeSet<>();
        allPeriods.addAll(commentsByMonth.keySet());
        allPeriods.addAll(votesByMonth.keySet());

        List<Map<String, Object>> participationTrend = allPeriods.stream()
                .map(period -> {
                    Map<String, Object> entry = new LinkedHashMap<>();
                    entry.put("period", period);
                    entry.put("comments", commentsByMonth.getOrDefault(period, 0L));
                    entry.put("votes", votesByMonth.getOrDefault(period, 0L));
                    return entry;
                })
                .collect(Collectors.toList());

        // ─── Topic distribution across all amendments ───
        Map<String, Long> topicDist = new LinkedHashMap<>();
        allAnalytics.stream()
                .filter(a -> a.getTopicClusters() != null)
                .flatMap(a -> a.getTopicClusters().stream())
                .forEach(cluster -> {
                    String topic = String.valueOf(cluster.getOrDefault("topic", "Unknown"));
                    topicDist.merge(topic, 1L, Long::sum);
                });

        return DashboardResponse.builder()
                .totalAmendments(totalAmendments)
                .activeAmendments(activeAmendments)
                .closedAmendments(closedAmendments)
                .totalUsers(totalUsers)
                .totalComments(totalComments)
                .totalVotes(totalVotes)
                .globalSentimentMean(globalSentiment)
                .globalSentimentDistribution(globalSentimentDistribution)
                .mostControversial(mostControversial)
                .participationTrend(participationTrend)
                .topicDistribution(topicDist)
                .build();
    }
}
