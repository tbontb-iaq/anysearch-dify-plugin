import json
from typing import Any, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .utils import call_anysearch, format_results_as_text


def _parse_params(raw: Any) -> dict:
    """Accept JSON ('{"type":"stock",...}') or flat 'type=stock,symbol=AAPL' strings."""
    if isinstance(raw, dict):
        return raw
    if not raw:
        return {}
    text = str(raw).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    result: dict[str, str] = {}
    for pair in text.split(","):
        if "=" in pair:
            key, _, value = pair.partition("=")
            key = key.strip()
            if key:
                result[key] = value.strip()
    return result


class AnySearchVerticalSearchTool(Tool):
    """Vertical domain search via AnySearch POST /v1/search with tag + params."""

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("anysearch_api_key")
        if not api_key:
            yield self.create_text_message(
                "AnySearch API key is missing. Please set it in the credentials."
            )
            return

        query = tool_parameters.get("query", "")
        tag = tool_parameters.get("tag", "")
        if not query or not tag:
            yield self.create_text_message(
                "Both 'query' and 'tag' are required for vertical search. "
                "Use the sub_domains tool to discover valid tags."
            )
            return

        payload: dict[str, Any] = {"query": query, "tag": tag}
        sub_domain_params = _parse_params(tool_parameters.get("params"))
        if sub_domain_params:
            payload["params"] = sub_domain_params

        max_results = tool_parameters.get("max_results") or 5
        try:
            max_results = max(1, min(int(max_results), 10))
        except (TypeError, ValueError):
            max_results = 5
        payload["max_results"] = max_results

        try:
            data = call_anysearch("/v1/search", api_key, payload=payload)
        except Exception as e:
            yield self.create_text_message(f"Error occurred while searching: {str(e)}")
            return

        results = data.get("results") or []
        if not results:
            yield self.create_text_message(
                f"No results found for '{query}' (tag {tag}) in AnySearch."
            )
            return

        yield self.create_json_message(
            {"query": query, "tag": tag, "results": results, "metadata": data.get("metadata") or {}}
        )
        yield self.create_text_message(format_results_as_text(results))
