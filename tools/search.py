from typing import Any, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .utils import call_anysearch, format_results_as_text


class AnySearchSearchTool(Tool):
    """General web search via AnySearch POST /v1/search."""

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
        if not query:
            yield self.create_text_message("Please input a query.")
            return

        max_results = tool_parameters.get("max_results") or 5
        try:
            max_results = max(1, min(int(max_results), 10))
        except (TypeError, ValueError):
            max_results = 5

        try:
            data = call_anysearch(
                "/v1/search",
                api_key,
                payload={"query": query, "max_results": max_results},
            )
        except Exception as e:
            yield self.create_text_message(f"Error occurred while searching: {str(e)}")
            return

        results = data.get("results") or []
        if not results:
            yield self.create_text_message(f"No results found for '{query}' in AnySearch.")
            return

        yield self.create_json_message(
            {"query": query, "results": results, "metadata": data.get("metadata") or {}}
        )
        yield self.create_text_message(format_results_as_text(results))
