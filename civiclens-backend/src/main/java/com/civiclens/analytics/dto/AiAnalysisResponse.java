package com.civiclens.analytics.dto;

import lombok.*;
import java.util.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiAnalysisResponse {
    private List<Double> sentimentScores;
    private Map<String, Integer> sentimentDistribution;
    private List<Map<String, Object>> sentimentTimeline;
    private List<Map<String, Object>> topicClusters;
    private Map<String, Integer> stanceCounts;
    private List<String> topSupporting;
    private List<String> topOpposing;
    private String policyBrief;
}
