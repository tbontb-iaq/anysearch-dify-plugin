from typing import Any, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .utils import call_anysearch


class AnySearchExtractTool(Tool):
    """Web page extraction via AnySearch POST /v1/extract (returns Markdown)."""

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("anysearch_api_key")
        if not api_key:
            yield self.create_text_message(
                "AnySearch API key is missing. Please set it in the credentials."
            )
            return

        url = tool_parameters.get("url", "")
        if not url:
            yield self.create_text_message("Please input a URL.")
            return

        try:
            data = call_anysearch("/v1/extract", api_key, payload={"url": url})
        except Exception as e:
            yield self.create_text_message(f"Error occurred while extracting: {str(e)}")
            return

        content = data.get("content") or ""
        if not content:
            yield self.create_text_message(f"No content extracted from '{url}'.")
            return

        yield self.create_json_message(
            {"url": data.get("url") or url, "title": data.get("title") or "", "content": content}
        )
        yield self.create_text_message(content)
