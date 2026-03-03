package com.civiclens.analytics.dto;

import lombok.*;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AiAnalysisRequest {
    private Long amendmentId;
    private String amendmentText;
    private List<String> comments;
}
