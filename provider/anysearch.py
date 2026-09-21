from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.search import AnySearchSearchTool


class AnySearchProvider(ToolProvider):
    def validate_credentials(self, credentials: dict) -> None:
        try:
            for _ in AnySearchSearchTool.from_credentials(
                credentials
            ).invoke_from_executor(
                tool_parameters={
                    "query": "test",
                    "max_results": 1,
                },
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
