"""
Analysis pipeline — orchestrates all AI models for a single analysis request.
Uses asyncio.gather() to run independent API calls in parallel.
"""
import asyncio
import logging
from models import sentiment, topic, classifier, summarizer

logger = logging.getLogger(__name__)


async def run_analysis(amendment_text: str, comments: list[str]) -> dict:
    """
    Run the full analysis pipeline on an amendment and its comments.
    Returns the complete analysis payload.
    """
    logger.info("Starting analysis pipeline for %d comments", len(comments))

    if not comments:
        return _empty_result()

    # Run sentiment, classification, and summarization in parallel (all are API calls)
    # Topic modeling is CPU-bound (TF-IDF) so it runs separately
    logger.info("Running sentiment, classification, summarization in parallel")
    sentiment_task = sentiment.analyze(comments)
    classification_task = classifier.classify(comments)
    summary_task = summarizer.summarize(amendment_text, comments)

    sentiment_scores, classification_result, policy_brief = await asyncio.gather(
        sentiment_task, classification_task, summary_task
    )

    # Sentiment post-processing
    sentiment_dist = sentiment.get_distribution(sentiment_scores)
    sentiment_timeline = _build_timeline(sentiment_scores)

    # Topic modeling (CPU-bound, runs in thread to not block event loop)
    logger.info("Running topic modeling")
    topic_clusters = await asyncio.to_thread(topic.extract_topics, comments)

    # Classification post-processing
    stance_counts = classification_result["stance_counts"]
    classified = classification_result["classified"]
    top_supporting = classifier.get_top_arguments(classified, "support", top_n=3)
    top_opposing = classifier.get_top_arguments(classified, "oppose", top_n=3)

    logger.info("Analysis pipeline completed successfully")

    return {
        "sentiment_scores": sentiment_scores,
        "sentiment_distribution": sentiment_dist,
        "sentiment_timeline": sentiment_timeline,
        "topic_clusters": topic_clusters,
        "stance_counts": stance_counts,
        "top_supporting": top_supporting,
        "top_opposing": top_opposing,
        "policy_brief": policy_brief,
    }


def _build_timeline(scores: list[float], buckets: int = 10) -> list[dict]:
    """Build a simple timeline by dividing scores into buckets."""
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
            "count": len(bucket),
        })
    return timeline


def _empty_result() -> dict:
    return {
        "sentiment_scores": [],
        "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0},
        "sentiment_timeline": [],
        "topic_clusters": [],
        "stance_counts": {"support": 0, "oppose": 0, "suggestion": 0, "neutral": 0},
        "top_supporting": [],
        "top_opposing": [],
        "policy_brief": "No comments available for analysis.",
    }
