from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    # This config tells Python: "Expect camelCase from Java, but use snake_case in Python"
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    
    amendment_id: int
    amendment_text: str
    comments: List[str]


class AnalysisResponse(BaseModel):
    # This config tells Python: "Send camelCase back to Java so the Frontend doesn't break"
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, serialize_by_alias=True)
    
    sentiment_scores: List[float]
    sentiment_distribution: dict
    sentiment_timeline: List[dict]
    topic_clusters: List[dict]
    stance_counts: dict
    top_supporting: List[str]
    top_opposing: List[str]
    policy_brief: str