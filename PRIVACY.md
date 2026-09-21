# Privacy Policy — AnySearch Plugin for Dify

This plugin sends the following data to the AnySearch API (`https://api.anysearch.com`) when its tools are invoked:

- **`search` / `vertical_search`**: the search query text (and, for vertical search, the selected tag and parameters).
- **`extract`**: the URL of the page to extract.
- **All requests**: the API key configured in the plugin credentials, sent as an `Authorization: Bearer` header.

What this plugin does **not** do:

- It does not collect, store, or log any user data itself.
- It does not send Dify workspace data, conversation content, or credentials other than the AnySearch API key to any party.
- It does not execute code, access the filesystem, or make requests to hosts other than `api.anysearch.com`.

AnySearch's own data handling (retention, logging, tracking) for queries sent to its API is described in the [AnySearch privacy documentation](https://anysearch.com). If you do not want queries or URLs to be processed by AnySearch, do not configure this plugin.
