package com.civiclens.comment;

import com.civiclens.amendment.Amendment;
import com.civiclens.user.User;
import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "comments", indexes = {
    @Index(name = "idx_comments_amendment_id", columnList = "amendment_id")
})
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Comment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "amendment_id", nullable = false)
    private Amendment amendment;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String body;

    @Column(name = "upvote_count", nullable = false)
    @Builder.Default
    private int upvoteCount = 0;

    @Column(name = "downvote_count", nullable = false)
    @Builder.Default
    private int downvoteCount = 0;

    @Column(name = "created_at", nullable = false, updatable = false)
    @Builder.Default
    private LocalDateTime createdAt = LocalDateTime.now();
}
