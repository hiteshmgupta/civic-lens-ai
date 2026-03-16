package com.civiclens.comment.dto;

import lombok.*;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommentResponse {
    private Long id;
    private String body;
    private String username;
    private int upvotes;
    private int downvotes;
    private LocalDateTime createdAt;
}
