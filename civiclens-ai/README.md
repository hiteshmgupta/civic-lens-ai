# CivicLens AI Service

Python microservice that handles all the NLP/ML analysis for CivicLens. Uses HuggingFace Inference API so no local model downloads are needed.

## What It Does

- **Sentiment Analysis** — Scores each comment from -1 to +1 using `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Summarization** — Generates policy briefs from public comments using `facebook/bart-large-cnn`
- **Argument Classification** — Zero-shot classification into support/oppose/suggestion/neutral via `facebook/bart-large-mnli`
- **Topic Modeling** — Groups comments into clusters using TF-IDF + KMeans (runs locally, no API)
- **Controversy Index** — Custom scoring formula: `C(a) = S · P · D · √E`

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

set HF_API_TOKEN=your_token     # Get free token at huggingface.co/settings/tokens
python -m uvicorn main:app --port 8000
```

Runs on **http://localhost:8000**. Health check: `GET /ai/health`

## API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/ai/health` | Health check |
| POST | `/ai/analyze` | Run full analysis on an amendment's comments |

## Tests

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

