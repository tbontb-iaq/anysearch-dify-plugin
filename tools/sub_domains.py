import json
from typing import Any, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .utils import call_anysearch


class AnySearchSubDomainsTool(Tool):
    """Discover vertical sub-domains via AnySearch GET /v1/sub-domains."""

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("anysearch_api_key")
        if not api_key:
            yield self.create_text_message(
                "AnySearch API key is missing. Please set it in the credentials."
            )
            return

        domain = tool_parameters.get("domain", "")
        if not domain:
            yield self.create_text_message("Please input a domain (e.g. finance).")
            return

        try:
            data = call_anysearch(
                "/v1/sub-domains", api_key, params=[("domain", domain)]
            )
        except Exception as e:
            yield self.create_text_message(f"Error occurred while listing sub-domains: {str(e)}")
            return

        payload = data.get("domains") or data
        yield self.create_json_message({"domain": domain, "domains": payload})
        yield self.create_text_message(
            f"```json\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n```"
        )
