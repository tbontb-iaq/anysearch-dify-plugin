import requests

BASE_URL = "https://api.anysearch.com"
TIMEOUT = 30


def call_anysearch(path: str, api_key: str, payload: dict | None = None, params: list | None = None) -> dict:
    """Call the AnySearch REST API and return its `data` payload.

    All endpoints answer with an envelope `{"code": 0, "message": ..., "data": ...}`;
    a non-zero `code` (or a non-dict body) is raised as an error.
    """
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    method = "POST" if payload is not None else "GET"
    resp = requests.request(
        method,
        f"{BASE_URL}{path}",
        json=payload,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    envelope = resp.json()
    if not isinstance(envelope, dict) or envelope.get("code", 0) != 0:
        message = envelope.get("message") if isinstance(envelope, dict) else "invalid response"
        raise RuntimeError(f"AnySearch API error: {message}")

    data = envelope.get("data")
    return data if isinstance(data, dict) else {}


def format_results_as_text(results: list) -> str:
    """Render search results as Markdown for text messages."""
    lines = []
    for i, result in enumerate(results, 1):
        if not isinstance(result, dict):
            continue
        title = result.get("title") or "(Untitled)"
        lines.append(f"{i}. [{title}]({result.get('url', '')})")
        snippet = result.get("snippet") or result.get("content") or ""
        if snippet:
            lines.append(f"   {snippet}")
        lines.append("")
    return "\n".join(lines).strip()
