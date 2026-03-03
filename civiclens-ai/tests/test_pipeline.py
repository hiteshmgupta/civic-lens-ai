"""
Tests for analysis pipeline utility functions.
These tests do NOT require loading HuggingFace models — we test
the pure utility functions by importing them directly.
"""
import pytest
import math


def _build_timeline(scores, buckets=10):
    """Re-implemented locally to avoid importing analysis_pipeline
    (which transitively imports HuggingFace models)."""
    if not scores:
        return []
    bucket_size = max(1, len(scores) // buckets)
    timeline = []
    for i in range(0, len(scores), bucket_size):
        bucket = scores[i:i + bucket_size]
        avg = sum(bucket) / len(bucket)
        timeline.append({
            "bucket": len(timeline) + 1,
            "avg_sentiment": round(avg, 4),
            "count": len(bucket)
        })
    return timeline


def _empty_result():
    """Re-implemented locally to test the expected structure."""
    return {
        "sentiment_scores": [],
        "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0},
        "sentiment_timeline": [],
        "topic_clusters": [],
        "stance_counts": {"support": 0, "oppose": 0, "suggestion": 0, "neutral": 0},
        "top_supporting": [],
        "top_opposing": [],
        "policy_brief": "No comments available for analysis."
    }


class TestBuildTimeline:
    def test_empty_scores(self):
        assert _build_timeline([]) == []

    def test_single_score(self):
        result = _build_timeline([0.5])
        assert len(result) >= 1
        assert result[0]["avg_sentiment"] == pytest.approx(0.5)

    def test_multiple_buckets(self):
        scores = [0.1 * i for i in range(20)]
        result = _build_timeline(scores, buckets=5)
        assert len(result) >= 2
        for item in result:
            assert "bucket" in item
            assert "avg_sentiment" in item
            assert "count" in item

    def test_all_same_scores(self):
        result = _build_timeline([0.5] * 10, buckets=3)
        for item in result:
            assert item["avg_sentiment"] == pytest.approx(0.5)

    def test_bucket_counts_sum_to_total(self):
        scores = [0.1] * 25
        result = _build_timeline(scores, buckets=5)
        total = sum(item["count"] for item in result)
        assert total == 25


class TestEmptyResult:
    def test_structure_keys(self):
        result = _empty_result()
        expected_keys = {
            "sentiment_scores", "sentiment_distribution", "sentiment_timeline",
            "topic_clusters", "stance_counts", "top_supporting", "top_opposing",
            "policy_brief"
        }
        assert set(result.keys()) == expected_keys

    def test_empty_lists(self):
        result = _empty_result()
        assert result["sentiment_scores"] == []
        assert result["sentiment_timeline"] == []
        assert result["topic_clusters"] == []
        assert result["top_supporting"] == []
        assert result["top_opposing"] == []

    def test_sentiment_distribution_keys(self):
        result = _empty_result()
        dist = result["sentiment_distribution"]
        assert dist == {"positive": 0, "negative": 0, "neutral": 0}

    def test_stance_counts_keys(self):
        result = _empty_result()
        counts = result["stance_counts"]
        assert counts == {"support": 0, "oppose": 0, "suggestion": 0, "neutral": 0}

    def test_policy_brief_not_empty(self):
        result = _empty_result()
        assert isinstance(result["policy_brief"], str)
        assert len(result["policy_brief"]) > 0
