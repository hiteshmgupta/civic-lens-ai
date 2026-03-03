"""
CivicLens AI Microservice — FastAPI application.
Provides sentiment analysis, topic modeling, argument classification,
summarization, and controversy index calculation.
"""
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import AnalysisRequest, AnalysisResponse
from services.analysis_pipeline import run_analysis
from models import sentiment, topic, classifier, summarizer
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("civiclens-ai")

models_loaded = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load models on startup."""
    global models_loaded
    logger.info("Pre-loading AI models...")
    start = time.time()
    try:
        sentiment.load_model()
        # Topic and classifier models are loaded lazily on first use
        # to reduce startup time (they're heavy)
        logger.info("Core models loaded in %.1fs", time.time() - start)
        models_loaded = True
    except Exception as e:
        logger.error("Model loading failed: %s", str(e))
        models_loaded = False
    yield
    logger.info("Shutting down AI service")


app = FastAPI(
    title="CivicLens AI Service",
    description="AI-powered legislative consultation analysis",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ai/health")
async def health_check():
    return {
        "status": "healthy" if models_loaded else "degraded",
        "models_loaded": models_loaded,
        "service": "civiclens-ai"
    }


@app.post("/ai/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    """
    Run full analysis pipeline on an amendment and its comments.
    """
    logger.info(
        "Analysis request: amendment_id=%d, comments=%d",
        request.amendment_id, len(request.comments)
    )

    start = time.time()
    try:
        result = run_analysis(request.amendment_text, request.comments)
        elapsed = time.time() - start
        logger.info(
            "Analysis completed in %.1fs for amendment %d",
            elapsed, request.amendment_id
        )
        return AnalysisResponse(**result)
    except Exception as e:
        logger.error("Analysis failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level="info"
    )
