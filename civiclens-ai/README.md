# CivicLens AI Service

AI-powered analysis microservice for the CivicLens platform.
Uses **HuggingFace Inference API** — no local model downloads, lightweight and fast to deploy (~200MB Docker image).

## Features

| Feature | Model / Method | Description |
|---|---|---|
| Sentiment Analysis | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Scores comments from -1 (negative) to +1 (positive) |
| Summarization | `facebook/bart-large-cnn` | Generates AI policy briefs from public feedback |
| Argument Classification | `facebook/bart-large-mnli` | Zero-shot: support / oppose / suggestion / neutral |
| Topic Modeling | TF-IDF + KMeans | Groups comments into topic clusters (no API calls) |
| Controversy Index | Custom formula | `C(a) = S · P · D · √E` combining sentiment, votes, stance, engagement |

## Prerequisites

| Tool | Version | Download Link | How to Verify |
|---|---|---|---|
| **Python** | 3.11+ | [python.org/downloads](https://www.python.org/downloads/) | `python --version` |
| **pip** | 23+ | Comes with Python | `pip --version` |

## Versions Used

| Dependency | Version |
|---|---|
| FastAPI | ≥0.109.0 |
| Uvicorn | ≥0.27.0 |
| Pydantic | ≥2.6.0 |
| httpx | ≥0.27.0 |
| scikit-learn | ≥1.4.0 |
| NumPy | ≥1.26.0 |

## Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows (Command Prompt)
# .venv\Scripts\Activate.ps1   # Windows (PowerShell)
# source .venv/bin/activate    # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your HuggingFace API token
#    Get a free token at: https://huggingface.co/settings/tokens
set HF_API_TOKEN=hf_your_token_here          # Windows CMD
# $env:HF_API_TOKEN="hf_your_token_here"     # Windows PowerShell
# export HF_API_TOKEN=hf_your_token_here      # macOS/Linux

# 4. Run the server
python -m uvicorn main:app --port 8000
```

The server starts at **http://localhost:8000**.
Health check: `http://localhost:8000/ai/health`

## API Endpoints

| Method | Path | Description |
|---|---|---|
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
|---|---|---|---|
| `HF_API_TOKEN` | Yes | — | HuggingFace API token ([get one free](https://huggingface.co/settings/tokens)) |
| `HOST` | No | `0.0.0.0` | Server bind address |
| `PORT` | No | `8000` | Server port |

## Deployment

Deployed on **Render** alongside the backend. Also supports Railway and Heroku.

- `Dockerfile` — python:3.11-slim
- `Procfile` — for PaaS platforms
- `render.yaml` — Render Blueprint

## Tests

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```
