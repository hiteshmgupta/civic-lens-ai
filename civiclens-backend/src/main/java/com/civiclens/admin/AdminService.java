package com.civiclens.admin;

import com.civiclens.admin.dto.DashboardResponse;
import com.civiclens.amendment.*;
import com.civiclens.analytics.*;
import com.civiclens.comment.CommentRepository;
import com.civiclens.user.UserRepository;
import com.civiclens.vote.VoteRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.*;
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
        long totalVotes = voteRepository.count();

        // Global sentiment mean
        List<AmendmentAnalytics> allAnalytics = analyticsRepository.findAll();
        double globalSentiment = allAnalytics.stream()
                .filter(a -> a.getSentimentMean() != null)
                .mapToDouble(AmendmentAnalytics::getSentimentMean)
                .average().orElse(0.0);

        // Most controversial
        List<Map<String, Object>> mostControversial = allAnalytics.stream()
                .filter(a -> a.getControversyScore() != null && a.getControversyScore() > 0)
                .sorted((a, b) -> Double.compare(b.getControversyScore(), a.getControversyScore()))
                .limit(5)
                .map(a -> {
                    Map<String, Object> map = new LinkedHashMap<>();
                    map.put("amendmentId", a.getAmendment().getId());
                    map.put("title", a.getAmendment().getTitle());
                    map.put("controversyScore", a.getControversyScore());
                    map.put("controversyLabel", a.getControversyLabel());
                    return map;
                })
                .collect(Collectors.toList());

        // Topic distribution across all amendments
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
                .mostControversial(mostControversial)
                .topicDistribution(topicDist)
                .build();
    }
}
