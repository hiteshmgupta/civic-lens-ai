"""
Shared async HTTP client for HuggingFace Inference API.
Handles retries, rate-limiting, and model loading waits.
"""
import asyncio
import logging
import httpx
from config import HF_API_URL, HF_API_TOKEN

logger = logging.getLogger(__name__)

_client: httpx.AsyncClient | None = None

MAX_RETRIES = 3
RETRY_BACKOFF = [1, 3, 10]  # seconds between retries
TIMEOUT = 120.0


def _headers() -> dict:
    if HF_API_TOKEN:
        return {"Authorization": f"Bearer {HF_API_TOKEN}"}
    return {}


async def get_client() -> httpx.AsyncClient:
    """Get or create the shared async HTTP client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(TIMEOUT),
            headers=_headers(),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _client


async def close_client():
    """Close the shared client (call on app shutdown)."""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


async def query(model: str, payload: dict) -> dict | list:
    """
    Send a request to HuggingFace Inference API with automatic retry.

    Args:
        model:   Model identifier (e.g. "facebook/bart-large-cnn")
        payload: JSON body (inputs, parameters, options)

    Returns:
        Parsed JSON response from HF API.

    Raises:
        RuntimeError if all retries are exhausted.
    """
    url = f"{HF_API_URL}/{model}"
    # Always ask HF to wait for the model to load
    payload.setdefault("options", {})["wait_for_model"] = True

    client = await get_client()
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = await client.post(url, json=payload)

            # Model still loading — wait and retry
            if response.status_code == 503:
                body = response.json()
                wait = body.get("estimated_time", RETRY_BACKOFF[attempt])
                logger.warning(
                    "Model %s loading, retry %d/%d in %.0fs",
                    model, attempt + 1, MAX_RETRIES, wait,
                )
                await asyncio.sleep(min(wait, 30))
                continue

            # Rate limited
            if response.status_code == 429:
                wait = RETRY_BACKOFF[attempt]
                logger.warning(
                    "Rate limited on %s, retry %d/%d in %ds",
                    model, attempt + 1, MAX_RETRIES, wait,
                )
                await asyncio.sleep(wait)
                continue

            response.raise_for_status()
            return response.json()

        except httpx.TimeoutException as e:
            last_error = e
            logger.warning("Timeout calling %s (attempt %d)", model, attempt + 1)
            await asyncio.sleep(RETRY_BACKOFF[attempt])
        except httpx.HTTPStatusError as e:
            last_error = e
            logger.error("HTTP %d from %s: %s", e.response.status_code, model, e.response.text[:200])
            if e.response.status_code < 500:
                raise RuntimeError(f"HF API error {e.response.status_code}: {e.response.text[:200]}") from e
            await asyncio.sleep(RETRY_BACKOFF[attempt])
        except Exception as e:
            last_error = e
            logger.error("Unexpected error calling %s: %s", model, str(e))
            await asyncio.sleep(RETRY_BACKOFF[attempt])

    raise RuntimeError(f"HF API call to {model} failed after {MAX_RETRIES} retries: {last_error}")
