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
     * Calculate Sentiment Dispersion S = Weighted Standard Deviation ∈ [0,1].
     */
    public double sentimentVariance(double[] sentimentScores, double[] weights) {
        if (sentimentScores == null || sentimentScores.length == 0)
            return 0.0;
        
        int n = sentimentScores.length;
        double weightSum = 0;
        double weightedMean = 0;

        for (int i = 0; i < n; i++) {
            double w = (weights != null && weights.length > i) ? weights[i] : 1.0;
            weightedMean += sentimentScores[i] * w;
            weightSum += w;
        }

        if (weightSum == 0) return 0.0;
        weightedMean /= weightSum;

        double weightedVariance = 0;
        for (int i = 0; i < n; i++) {
            double w = (weights != null && weights.length > i) ? weights[i] : 1.0;
            weightedVariance += w * Math.pow(sentimentScores[i] - weightedMean, 2);
        }
        weightedVariance /= weightSum;

        // Use Standard Deviation to boost small values, bounded [0,1]
        double stdev = Math.sqrt(weightedVariance);
        return Math.min(stdev, 1.0);
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
     */
    public double stanceEntropy(Map<String, Integer> stanceCounts) {
        if (stanceCounts == null || stanceCounts.isEmpty())
            return 0.0;
        
        int K = stanceCounts.size();
        int total = stanceCounts.values().stream().mapToInt(Integer::intValue).sum();
        if (total == 0)
            return 0.0;

        if (K <= 1)
            return 0.1; // Base case so it's not entirely 0

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
     * Calculate final Controversy Score C(a) ∈ [0,1].
     * Uses an arithmetic average so a single 0 doesn't flatline the score.
     */
    public double controversyScore(double S, double P, double D, double E) {
        // Boost E
        double eBoosted = Math.sqrt(E);
        double score = (S + P + D + eBoosted) / 4.0;
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
