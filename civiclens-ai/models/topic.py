"""
Topic Modeling using TF-IDF + KMeans clustering.
Lightweight alternative to BERTopic — no large model downloads needed.
"""
import logging
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


def load_model():
    """No-op — TF-IDF/KMeans are fitted per-request."""
    logger.info("Topic modeling: using TF-IDF + KMeans (lightweight)")


def extract_topics(texts: list[str]) -> list[dict]:
    """
    Extract topic clusters from a list of texts.
    Returns list of {topic: str, size: int, keywords: list[str]}.
    """
    if not texts or len(texts) < 5:
        return [{"topic": "General Discussion", "size": len(texts), "keywords": []}]

    try:
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words="english",
            min_df=2,
            max_df=0.95,
            ngram_range=(1, 2)
        )
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()

        # Determine number of clusters (2-10, based on data size)
        n_clusters = min(max(2, int(math.sqrt(len(texts) / 2))), 10)

        # KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(tfidf_matrix)

        # Extract top keywords per cluster
        clusters = []
        for cluster_id in range(n_clusters):
            cluster_mask = labels == cluster_id
            cluster_size = int(cluster_mask.sum())

            if cluster_size == 0:
                continue

            # Get centroid and find top terms
            centroid = kmeans.cluster_centers_[cluster_id]
            top_indices = centroid.argsort()[-5:][::-1]
            keywords = [feature_names[i] for i in top_indices]

            clusters.append({
                "topic": " | ".join(keywords[:3]),
                "size": cluster_size,
                "keywords": list(keywords)
            })

        clusters.sort(key=lambda x: x["size"], reverse=True)
        return clusters[:10]

    except Exception as e:
        logger.error("Topic modeling failed: %s", str(e))
        return [{"topic": "General Discussion", "size": len(texts), "keywords": []}]
