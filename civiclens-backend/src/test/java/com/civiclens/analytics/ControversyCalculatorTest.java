package com.civiclens.analytics;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Tests for the Controversy Index mathematical components.
 * Verifies C(a) = S · P · D · √E against known values.
 */
class ControversyCalculatorTest {

    private ControversyCalculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new ControversyCalculator();
    }

    // Vote Polarity: P = 1 − |U − D| / (U + D) ∈ [0,1]

    @Test
    @DisplayName("P = 1.0 when votes are perfectly split (50/50)")
    void votePolarity_evenSplit_returnsOne() {
        assertEquals(1.0, calculator.votePolarity(50, 50), 1e-9);
    }

    @Test
    @DisplayName("P = 0.0 when votes are unanimous")
    void votePolarity_unanimous_returnsZero() {
        assertEquals(0.0, calculator.votePolarity(100, 0), 1e-9);
        assertEquals(0.0, calculator.votePolarity(0, 100), 1e-9);
    }

    @Test
    @DisplayName("P = 0.0 when no votes exist")
    void votePolarity_noVotes_returnsZero() {
        assertEquals(0.0, calculator.votePolarity(0, 0), 1e-9);
    }

    @Test
    @DisplayName("P is between 0 and 1 for typical vote distributions")
    void votePolarity_typicalDistribution() {
        double p = calculator.votePolarity(60, 40);
        // P = 1 - |60-40|/100 = 1 - 0.2 = 0.8
        assertEquals(0.8, p, 1e-9);
    }

    // Sentiment Variance: S = σ² ∈ [0,1]

    @Test
    @DisplayName("S = 0.0 for empty scores array")
    void sentimentVariance_empty_returnsZero() {
        assertEquals(0.0, calculator.sentimentVariance(new double[] {}, null), 1e-9);
        assertEquals(0.0, calculator.sentimentVariance(null, null), 1e-9);
    }

    @Test
    @DisplayName("S = 0.0 for uniform sentiment (no variance)")
    void sentimentVariance_uniform_returnsZero() {
        assertEquals(0.0, calculator.sentimentVariance(new double[] { 0.5, 0.5, 0.5 }, null), 1e-9);
    }

    @Test
    @DisplayName("S > 0 for mixed sentiment scores")
    void sentimentVariance_mixed_returnsPositive() {
        // scores: -1, 1 → mean=0, variance = (1+1)/2 = 1.0
        double s = calculator.sentimentVariance(new double[] { -1.0, 1.0 }, null);
        assertEquals(1.0, s, 1e-9);
    }

    @Test
    @DisplayName("S is bounded to [0,1]")
    void sentimentVariance_bounded() {
        double s = calculator.sentimentVariance(new double[] { -1.0, 1.0, -1.0, 1.0 }, null);
        assertTrue(s >= 0 && s <= 1.0, "Variance should be in [0,1], got: " + s);
    }

    // Sentiment Mean

    @Test
    @DisplayName("Mean of empty scores is 0")
    void sentimentMean_empty() {
        assertEquals(0.0, calculator.sentimentMean(new double[] {}), 1e-9);
        assertEquals(0.0, calculator.sentimentMean(null), 1e-9);
    }

    @Test
    @DisplayName("Mean is correctly calculated")
    void sentimentMean_typical() {
        assertEquals(0.5, calculator.sentimentMean(new double[] { 0.0, 1.0 }), 1e-9);
    }

    // Stance Entropy: D = H / log(K) ∈ [0,1]

    @Test
    @DisplayName("D = 1.0 for perfectly even distribution")
    void stanceEntropy_evenDistribution_returnsOne() {
        Map<String, Integer> counts = new HashMap<>();
        counts.put("support", 25);
        counts.put("oppose", 25);
        counts.put("suggestion", 25);
        counts.put("neutral", 25);
        assertEquals(1.0, calculator.stanceEntropy(counts), 1e-9);
    }

    @Test
    @DisplayName("D = 0.1 for single category")
    void stanceEntropy_singleCategory_returnsLowValue() {
        Map<String, Integer> counts = Map.of("support", 100);
        assertEquals(0.1, calculator.stanceEntropy(counts), 1e-9);
    }

    @Test
    @DisplayName("D = 0.0 for empty map")
    void stanceEntropy_empty_returnsZero() {
        assertEquals(0.0, calculator.stanceEntropy(new HashMap<>()), 1e-9);
        assertEquals(0.0, calculator.stanceEntropy(null), 1e-9);
    }

    @Test
    @DisplayName("D is between 0 and 1 for skewed distribution")
    void stanceEntropy_skewed() {
        Map<String, Integer> counts = new HashMap<>();
        counts.put("support", 90);
        counts.put("oppose", 10);
        double d = calculator.stanceEntropy(counts);
        assertTrue(d > 0 && d < 1.0, "Entropy should be in (0,1) for skewed case, got: " + d);
    }

    // Engagement Intensity: E = log(1+n) / log(1+n_max) ∈ [0,1]

    @Test
    @DisplayName("E = 0.0 when no comments")
    void engagementIntensity_zero() {
        assertEquals(0.0, calculator.engagementIntensity(0, 100), 1e-9);
    }

    @Test
    @DisplayName("E = 1.0 when comments equal max")
    void engagementIntensity_max() {
        assertEquals(1.0, calculator.engagementIntensity(100, 100), 1e-9);
    }

    @Test
    @DisplayName("E = 0.0 when max is zero")
    void engagementIntensity_zeroMax() {
        assertEquals(0.0, calculator.engagementIntensity(50, 0), 1e-9);
    }

    @Test
    @DisplayName("E is between 0 and 1 for typical values")
    void engagementIntensity_typical() {
        double e = calculator.engagementIntensity(50, 200);
        assertTrue(e > 0 && e < 1.0, "Engagement should be in (0,1), got: " + e);
    }

    // Controversy Score: C(a) = S · P · D · √E ∈ [0,1]

    @Test
    @DisplayName("C is non-zero because it's an average now")
    void controversyScore_zeroComponent_isAverage() {
        assertEquals(0.25, calculator.controversyScore(1.0, 0.0, 0.0, 0.0), 1e-9);
    }

    @Test
    @DisplayName("C is maximum when all components are 1")
    void controversyScore_allMax() {
        assertEquals(1.0, calculator.controversyScore(1.0, 1.0, 1.0, 1.0), 1e-9);
    }

    @Test
    @DisplayName("C is clamped to [0,1]")
    void controversyScore_clamped() {
        double c = calculator.controversyScore(0.5, 0.8, 0.7, 0.6);
        assertTrue(c >= 0 && c <= 1.0, "Score should be in [0,1], got: " + c);
    }

    // Controversy Label thresholds

    @Test
    @DisplayName("Labels map correctly to score ranges")
    void controversyLabel_allThresholds() {
        assertEquals("Low", calculator.controversyLabel(0.0));
        assertEquals("Low", calculator.controversyLabel(0.24));
        assertEquals("Moderate", calculator.controversyLabel(0.25));
        assertEquals("Moderate", calculator.controversyLabel(0.49));
        assertEquals("High", calculator.controversyLabel(0.50));
        assertEquals("High", calculator.controversyLabel(0.74));
        assertEquals("Extreme", calculator.controversyLabel(0.75));
        assertEquals("Extreme", calculator.controversyLabel(1.0));
    }
}
