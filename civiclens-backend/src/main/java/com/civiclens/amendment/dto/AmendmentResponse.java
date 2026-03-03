package com.civiclens.amendment.dto;

import lombok.*;
import java.time.LocalDateTime;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class AmendmentResponse {
    private Long id;
    private String title;
    private String body;
    private String category;
    private String status;
    private LocalDateTime createdAt;
    private LocalDateTime closesAt;
    private String createdByUsername;
    private int upvotes;
    private int downvotes;
    private int commentCount;
    private Double sentimentMean;
    private Double controversyScore;
    private String controversyLabel;
}
