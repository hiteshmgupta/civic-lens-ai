package com.civiclens.analytics;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * Implements the Controversy Index functional:
 * C(a) = S · P · D · √E
 *
 * Where:
 * P = 1 − |U − D| / (U + D) Vote Polarity Symmetry ∈ [0,1]
 * S = σ² (sentiment variance) Sentiment Dispersion ∈ [0,1]
 * D = H / log(K) Normalized Stance Entropy ∈ [0,1]
 * E = log(1 + n) / log(1 + n_max) Engagement Intensity ∈ [0,1]
 */
@Component
@Slf4j
public class ControversyCalculator {

    /**
     * Calculate Vote Polarity Symmetry P ∈ [0,1].
     * P = 1 when votes are evenly split. P = 0 when unanimous.
     */
    public double votePolarity(int upvotes, int downvotes) {
        int total = upvotes + downvotes;
        if (total == 0)
            return 0.0;
        return 1.0 - (double) Math.abs(upvotes - downvotes) / total;
    }

    /**
     * Calculate Sentiment Dispersion S = σ² ∈ [0,1].
     * Variance of sentiment scores where each s_i ∈ [-1, 1].
     */
    public double sentimentVariance(double[] sentimentScores) {
        if (sentimentScores == null || sentimentScores.length == 0)
            return 0.0;
        int n = sentimentScores.length;
        double mean = 0;
        for (double s : sentimentScores)
            mean += s;
        mean /= n;
        double variance = 0;
        for (double s : sentimentScores)
            variance += (s - mean) * (s - mean);
        variance /= n;
        return Math.min(variance, 1.0); // bounded [0,1]
    }

    /**
     * Calculate mean of sentiment scores.
     */
    public double sentimentMean(double[] sentimentScores) {
        if (sentimentScores == null || sentimentScores.length == 0)
            return 0.0;
        double sum = 0;
        for (double s : sentimentScores)
            sum += s;
        return sum / sentimentScores.length;
    }

    /**
     * Calculate Normalized Stance Entropy D ∈ [0,1].
     * D = H / log(K) where H = -Σ(pk · log(pk))
     * K = number of stance groups
     */
    public double stanceEntropy(Map<String, Integer> stanceCounts) {
        if (stanceCounts == null || stanceCounts.isEmpty())
            return 0.0;
        int K = stanceCounts.size();
        if (K <= 1)
            return 0.0;

        int total = stanceCounts.values().stream().mapToInt(Integer::intValue).sum();
        if (total == 0)
            return 0.0;

        double H = 0;
        for (int count : stanceCounts.values()) {
            if (count > 0) {
                double pk = (double) count / total;
                H -= pk * Math.log(pk);
            }
        }
        double maxEntropy = Math.log(K);
        return maxEntropy > 0 ? H / maxEntropy : 0.0;
    }

    /**
     * Calculate Engagement Intensity E ∈ [0,1].
     * E = log(1 + n) / log(1 + n_max)
     */
    public double engagementIntensity(int commentCount, int maxCommentCount) {
        if (maxCommentCount <= 0)
            return 0.0;
        return Math.log(1.0 + commentCount) / Math.log(1.0 + maxCommentCount);
    }

    /**
     * Calculate final Controversy Score C(a) = S · P · D · √E ∈ [0,1].
     */
    public double controversyScore(double S, double P, double D, double E) {
        double score = S * P * D * Math.sqrt(E);
        return Math.max(0, Math.min(1, score)); // clamp to [0,1]
    }

    /**
     * Interpret controversy score as human-readable label.
     */
    public String controversyLabel(double score) {
        if (score < 0.25)
            return "Low";
        if (score < 0.50)
            return "Moderate";
        if (score < 0.75)
            return "High";
        return "Extreme";
    }

}
