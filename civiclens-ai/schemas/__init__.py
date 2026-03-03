from pydantic import BaseModel
from typing import List, Optional


class AnalysisRequest(BaseModel):
    amendment_id: int
    amendment_text: str
    comments: List[str]


class AnalysisResponse(BaseModel):
    sentiment_scores: List[float]
    sentiment_distribution: dict
    sentiment_timeline: List[dict]
    topic_clusters: List[dict]
    stance_counts: dict
    top_supporting: List[str]
    top_opposing: List[str]
    policy_brief: str
