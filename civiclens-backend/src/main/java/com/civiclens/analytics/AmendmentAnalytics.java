package com.civiclens.analytics;

import com.civiclens.amendment.Amendment;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import java.time.LocalDateTime;
import java.util.*;

@Entity
@Table(name = "amendment_analytics")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class AmendmentAnalytics {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "amendment_id", nullable = false, unique = true)
    private Amendment amendment;

    @Column(name = "sentiment_mean")
    @Builder.Default
    private Double sentimentMean = 0.0;

    @Column(name = "sentiment_variance")
    @Builder.Default
    private Double sentimentVariance = 0.0;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "sentiment_distribution", columnDefinition = "jsonb")
    @Builder.Default
    private Map<String, Integer> sentimentDistribution = new HashMap<>();

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "sentiment_timeline", columnDefinition = "jsonb")
    @Builder.Default
    private List<Map<String, Object>> sentimentTimeline = new ArrayList<>();

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "topic_clusters", columnDefinition = "jsonb")
    @Builder.Default
    private List<Map<String, Object>> topicClusters = new ArrayList<>();

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "top_supporting", columnDefinition = "jsonb")
    @Builder.Default
    private List<String> topSupporting = new ArrayList<>();

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "top_opposing", columnDefinition = "jsonb")
    @Builder.Default
    private List<String> topOpposing = new ArrayList<>();

    @Column(name = "total_comments")
    @Builder.Default
    private Integer totalComments = 0;

    @Column(name = "total_votes")
    @Builder.Default
    private Integer totalVotes = 0;

    @Builder.Default
    private Integer upvotes = 0;

    @Builder.Default
    private Integer downvotes = 0;

    @Column(name = "vote_polarity")
    @Builder.Default
    private Double votePolarity = 0.0;

    @Column(name = "stance_entropy")
    @Builder.Default
    private Double stanceEntropy = 0.0;

    @Column(name = "engagement_score")
    @Builder.Default
    private Double engagementScore = 0.0;

    @Column(name = "controversy_score")
    @Builder.Default
    private Double controversyScore = 0.0;

    @Column(name = "controversy_label", length = 20)
    @Builder.Default
    private String controversyLabel = "Low";

    @Column(name = "policy_brief", columnDefinition = "TEXT")
    private String policyBrief;

    @Column(name = "last_computed_at")
    @Builder.Default
    private LocalDateTime lastComputedAt = LocalDateTime.now();
}
