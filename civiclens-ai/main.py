"""
CivicLens AI Microservice — FastAPI application.
Provides sentiment analysis, topic modeling, argument classification,
summarization, and controversy index calculation.

Uses HuggingFace Inference API — no local model downloads needed.
"""
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import AnalysisRequest, AnalysisResponse
from services.analysis_pipeline import run_analysis
import config
import hf_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("civiclens-ai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage shared resources (httpx client) on startup/shutdown."""
    logger.info("Starting CivicLens AI service (HF Inference API mode)")
    yield
    await hf_client.close_client()
    logger.info("CivicLens AI service shut down")


app = FastAPI(
    title="CivicLens AI Service",
    description="AI-powered legislative consultation analysis (HF Inference API)",
    version="0.3.0",
    lifespan=lifespan,
)

# Only the backend should call this service — restrict origins
_allowed_origins = [
    "http://localhost:8080",
    "https://civiclens-backend-j5q2.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/ai/health")
async def health_check():
    has_token = bool(config.HF_API_TOKEN)
    return {
        "status": "healthy" if has_token else "degraded (no HF_API_TOKEN)",
        "hf_api_token_set": has_token,
        "service": "civiclens-ai",
        "mode": "huggingface-inference-api",
        "version": "0.3.0",
    }


@app.post("/ai/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    """
    Run full analysis pipeline on an amendment and its comments.
    """
    logger.info(
        "Analysis request: amendment_id=%d, comments=%d",
        request.amendment_id, len(request.comments),
    )

    start = time.time()
    try:
        result = await run_analysis(request.amendment_text, request.comments)
        elapsed = time.time() - start
        logger.info(
            "Analysis completed in %.1fs for amendment %d",
            elapsed, request.amendment_id,
        )
        return AnalysisResponse(**result)
    except Exception as e:
        logger.error("Analysis failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Analysis failed. Check server logs for details.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level="info",
    )
