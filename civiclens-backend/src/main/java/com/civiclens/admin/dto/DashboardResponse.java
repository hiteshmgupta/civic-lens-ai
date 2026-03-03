package com.civiclens.admin.dto;

import lombok.*;
import java.util.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DashboardResponse {
    private long totalAmendments;
    private long activeAmendments;
    private long closedAmendments;
    private long totalUsers;
    private long totalComments;
    private long totalVotes;
    private Double globalSentimentMean;
    private List<Map<String, Object>> mostControversial;
    private List<Map<String, Object>> participationTrend;
    private Map<String, Long> topicDistribution;
}
