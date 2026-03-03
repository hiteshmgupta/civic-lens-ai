package com.civiclens.analytics.dto;

import lombok.*;
import java.util.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AnalyticsResponse {
    private Long amendmentId;
    private Double sentimentMean;
    private Double sentimentVariance;
    private Map<String, Integer> sentimentDistribution;
    private List<Map<String, Object>> sentimentTimeline;
    private List<Map<String, Object>> topicClusters;
    private List<String> topSupporting;
    private List<String> topOpposing;
    private Integer totalComments;
    private Integer totalVotes;
    private Integer upvotes;
    private Integer downvotes;
    private Double votePolarity;
    private Double stanceEntropy;
    private Double engagementScore;
    private Double controversyScore;
    private String controversyLabel;
    private String policyBrief;
}
