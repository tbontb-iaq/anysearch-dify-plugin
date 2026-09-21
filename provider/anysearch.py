from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.utils import call_anysearch


class AnySearchProvider(ToolProvider):
    def validate_credentials(self, credentials: dict) -> None:
        api_key = credentials.get("anysearch_api_key", "")
        try:
            # The tool layer yields error text instead of raising (house
            # style, like tavily), so iterating a tool's messages would
            # accept invalid keys. Validate against the API directly: a
            # 1-result search raises on HTTP errors and on non-zero
            # envelope codes (e.g. 401 "Invalid API key.").
            call_anysearch(
                "/v1/search",
                api_key,
                payload={"query": "test", "max_results": 1},
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
