"""
Tests for the shared HuggingFace Inference API client.
Uses mocked HTTP responses to test retry logic, rate limiting, etc.
"""
import pytest
import httpx
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock


# We need to patch hf_client at module level
@pytest.fixture(autouse=True)
def reset_client():
    """Reset the global client between tests."""
    import hf_client
    hf_client._client = None
    yield
    if hf_client._client and not hf_client._client.is_closed:
        asyncio.get_event_loop().run_until_complete(hf_client.close_client())


@pytest.mark.asyncio
async def test_query_success():
    """Test a successful API call."""
    import hf_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"label": "positive", "score": 0.9}]
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = mock_response
    mock_client.is_closed = False

    hf_client._client = mock_client

    result = await hf_client.query("test-model", {"inputs": "hello"})
    assert result == [{"label": "positive", "score": 0.9}]
    mock_client.post.assert_called_once()


@pytest.mark.asyncio
async def test_query_retry_on_503():
    """Test retry when model is loading (503)."""
    import hf_client

    loading_response = MagicMock()
    loading_response.status_code = 503
    loading_response.json.return_value = {"estimated_time": 0.1}

    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {"result": "ok"}
    success_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.side_effect = [loading_response, success_response]
    mock_client.is_closed = False

    hf_client._client = mock_client

    result = await hf_client.query("test-model", {"inputs": "hello"})
    assert result == {"result": "ok"}
    assert mock_client.post.call_count == 2


@pytest.mark.asyncio
async def test_query_retry_on_429():
    """Test retry on rate limit (429)."""
    import hf_client

    rate_limit_response = MagicMock()
    rate_limit_response.status_code = 429

    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {"result": "ok"}
    success_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.side_effect = [rate_limit_response, success_response]
    mock_client.is_closed = False

    hf_client._client = mock_client
    # Reduce retry backoff for test speed
    original_backoff = hf_client.RETRY_BACKOFF
    hf_client.RETRY_BACKOFF = [0.01, 0.01, 0.01]

    try:
        result = await hf_client.query("test-model", {"inputs": "hello"})
        assert result == {"result": "ok"}
        assert mock_client.post.call_count == 2
    finally:
        hf_client.RETRY_BACKOFF = original_backoff


@pytest.mark.asyncio
async def test_query_all_retries_exhausted():
    """Test RuntimeError after all retries are exhausted."""
    import hf_client

    loading_response = MagicMock()
    loading_response.status_code = 503
    loading_response.json.return_value = {"estimated_time": 0.01}

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = loading_response
    mock_client.is_closed = False

    hf_client._client = mock_client
    original_backoff = hf_client.RETRY_BACKOFF
    hf_client.RETRY_BACKOFF = [0.01, 0.01, 0.01]

    try:
        with pytest.raises(RuntimeError, match="failed after"):
            await hf_client.query("test-model", {"inputs": "hello"})
        assert mock_client.post.call_count == 3
    finally:
        hf_client.RETRY_BACKOFF = original_backoff


@pytest.mark.asyncio
async def test_query_sets_wait_for_model():
    """Test that wait_for_model option is always set."""
    import hf_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = mock_response
    mock_client.is_closed = False

    hf_client._client = mock_client

    await hf_client.query("test-model", {"inputs": "test"})

    call_args = mock_client.post.call_args
    payload = call_args.kwargs.get("json", call_args[1].get("json", {}))
    assert payload.get("options", {}).get("wait_for_model") is True
