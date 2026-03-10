"""
Tests for async model modules (sentiment, classifier, summarizer).
Uses mocked hf_client.query() to test without real API calls.
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_sentiment_analyze_empty():
    """Sentiment analyze returns empty list for empty input."""
    from models.sentiment import analyze
    assert await analyze([]) == []


@pytest.mark.asyncio
async def test_sentiment_analyze_success():
    """Sentiment analyze converts API results to scores."""
    mock_result = [
        [{"label": "positive", "score": 0.8}, {"label": "negative", "score": 0.1}, {"label": "neutral", "score": 0.1}],
        [{"label": "negative", "score": 0.7}, {"label": "positive", "score": 0.2}, {"label": "neutral", "score": 0.1}],
    ]

    with patch("models.sentiment.hf_client") as mock_hf:
        mock_hf.query = AsyncMock(return_value=mock_result)
        scores = await (await _import_analyze())( ["good", "bad"])

    # First score: 0.8 - 0.1 = 0.7, Second: 0.2 - 0.7 = -0.5
    assert len(scores) == 2
    assert scores[0] == pytest.approx(0.7)
    assert scores[1] == pytest.approx(-0.5)


@pytest.mark.asyncio
async def test_sentiment_analyze_api_failure_returns_neutral():
    """Sentiment analyze returns neutral (0.0) on API failure."""
    with patch("models.sentiment.hf_client") as mock_hf:
        mock_hf.query = AsyncMock(side_effect=RuntimeError("API down"))
        from models.sentiment import analyze
        scores = await analyze(["test text"])

    assert scores == [0.0]


def test_sentiment_distribution():
    """Test sentiment distribution counting."""
    from models.sentiment import get_distribution
    scores = [0.5, -0.3, 0.0, 0.2, -0.5]
    dist = get_distribution(scores)
    assert dist["positive"] == 2
    assert dist["negative"] == 2
    assert dist["neutral"] == 1


@pytest.mark.asyncio
async def test_classifier_empty():
    """Classifier returns empty counts for empty input."""
    from models.classifier import classify
    result = await classify([])
    assert result["stance_counts"]["support"] == 0
    assert result["classified"] == []


@pytest.mark.asyncio
async def test_classifier_success():
    """Classifier correctly counts stances."""
    with patch("models.classifier.hf_client") as mock_hf:
        mock_hf.query = AsyncMock(side_effect=[
            {"labels": ["support", "oppose", "neutral", "suggestion"], "scores": [0.7, 0.2, 0.05, 0.05]},
            {"labels": ["oppose", "support", "neutral", "suggestion"], "scores": [0.6, 0.2, 0.1, 0.1]},
        ])
        from models.classifier import classify
        result = await classify(["I agree", "I disagree"])

    assert result["stance_counts"]["support"] == 1
    assert result["stance_counts"]["oppose"] == 1
    assert len(result["classified"]) == 2


@pytest.mark.asyncio
async def test_summarizer_success():
    """Summarizer returns summary text from API."""
    with patch("models.summarizer.hf_client") as mock_hf:
        mock_hf.query = AsyncMock(return_value=[{"summary_text": "Test summary."}])
        from models.summarizer import summarize
        result = await summarize("Amendment text", ["Comment 1", "Comment 2"])

    assert result == "Test summary."


@pytest.mark.asyncio
async def test_summarizer_api_failure():
    """Summarizer returns fallback message on failure."""
    with patch("models.summarizer.hf_client") as mock_hf:
        mock_hf.query = AsyncMock(side_effect=RuntimeError("API down"))
        from models.summarizer import summarize
        result = await summarize("Amendment text", ["Comment 1"])

    assert "failed" in result.lower()


def test_classifier_get_top_arguments():
    """Test extracting top arguments by label."""
    from models.classifier import get_top_arguments
    classified = [("arg1", "support"), ("arg2", "oppose"), ("arg3", "support")]
    top = get_top_arguments(classified, "support", top_n=2)
    assert top == ["arg1", "arg3"]


async def _import_analyze():
    """Helper to import analyze after patching."""
    from models.sentiment import analyze
    return analyze
