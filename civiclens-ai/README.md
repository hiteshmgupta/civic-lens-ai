# CivicLens AI Service

AI-powered analysis microservice for the CivicLens platform.  
Uses **HuggingFace Inference API** — no local model downloads, lightweight and fast to deploy.

## Features

- **Sentiment Analysis** — cardiffnlp/twitter-roberta-base-sentiment-latest
- **Summarization** — facebook/bart-large-cnn (policy brief generation)
- **Argument Classification** — facebook/bart-large-mnli (zero-shot: support/oppose/suggestion/neutral)
- **Topic Modeling** — TF-IDF + KMeans (lightweight, no API calls)
- **Controversy Index** — custom formula: C(a) = S · P · D · √E

## Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your HuggingFace API token
set HF_API_TOKEN=hf_your_token_here          # Windows
# export HF_API_TOKEN=hf_your_token_here     # macOS/Linux

# 4. Run the server
python -m uvicorn main:app --port 8000
```

Health check: `http://localhost:8000/ai/health`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/ai/health` | Health check (shows HF token status) |
| POST | `/ai/analyze` | Run full analysis pipeline |

### POST `/ai/analyze` — Request Body

```json
{
  "amendment_id": 1,
  "amendment_text": "The proposed amendment text...",
  "comments": ["Comment 1", "Comment 2", "Comment 3"]
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HF_API_TOKEN` | Yes | — | HuggingFace API token ([get one free](https://huggingface.co/settings/tokens)) |
| `HOST` | No | `0.0.0.0` | Server bind address |
| `PORT` | No | `8000` | Server port |

## Deployment

Ready for one-click deploy on Render, Railway, or Heroku:
- `Dockerfile` — python:3.11-slim (~200MB image)
- `Procfile` — for PaaS platforms
- `render.yaml` — Render Blueprint

## Tests

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```
