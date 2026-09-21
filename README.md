# AnySearch Tools for Dify

[AnySearch](https://anysearch.com) is a real-time search service for AI agents: general web search, vertical domain search, and full-page content extraction.

## Available Actions

| Tool | Description |
| --- | --- |
| `search` | Real-time general web search |
| `vertical_search` | Vertical domain search (finance, academic, health, code, ...) with structured params |
| `extract` | Extract a web page's full content as clean Markdown |
| `sub_domains` | Discover the vertical sub-domain tags and their required parameters for a domain |

## Configuration

1. Get an API key from the [AnySearch console](https://anysearch.com/console/api-keys) (the API also has an anonymous tier with lower rate limits; a key lifts the limits).
2. Install this plugin from the Dify Marketplace (or via local `.difypkg`).
3. Enter the API key in the plugin's credential setup.
4. Add any of the tools above to your agent/workflow.

## Maintenance Notes

Development notes for future maintainers of this plugin:

- Privacy: see [PRIVACY.md](PRIVACY.md). No user data is collected, stored, or
  logged by the plugin itself; queries/URLs and the API key are sent to
  `api.anysearch.com` only.
- API base: `https://api.anysearch.com`. All endpoints answer with an envelope
  `{"code": 0, "message": ..., "request_id": ..., "data": ...}`; a non-zero
  `code` is an API error even on HTTP 200 — `tools/utils.py:call_anysearch`
  centralizes this handling and raises `RuntimeError(message)`.
- Endpoints used: `POST /v1/search` (`query`, optional `tag` + `params` for
  vertical search, `max_results` 1-10), `POST /v1/extract` (`url`),
  `GET /v1/sub-domains?domain=` (returns `data.domains[]` with each
  sub-domain's `params` and their `required` flags).
- `vertical_search.params` accepts either a JSON object string or a flat
  `key=value,key=value` string (see `_parse_params`); parameters marked
  `required` by `sub_domains` must all be provided, using an empty string
  value when not applicable.
- Layout follows the standard tool-plugin structure: `manifest.yaml`,
  `provider/` (credential declaration + validation via a live 1-result
  search), `tools/` (one yaml + one module per tool), `main.py` entrypoint.
- Formatting/lint: `uv run black . -C -l 100 && uv run ruff check --fix`.

## Resources

- [AnySearch](https://anysearch.com)
- [Source repository](https://github.com/tbontb-iaq/anysearch-dify-plugin)
- [API keys](https://anysearch.com/console/api-keys)
- [Dify Marketplace](https://market.dify.ai)
