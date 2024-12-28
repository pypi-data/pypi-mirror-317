![Python >= 3.8](https://img.shields.io/badge/python->=3.8-red.svg) [![](https://badgen.net/github/release/deedy5/searxng_search)](https://github.com/deedy5/searxng_search/releases) [![](https://badge.fury.io/py/searxng-search.svg)](https://pypi.org/project/searxng-search) [![Downloads](https://static.pepy.tech/badge/searxng-search)](https://pepy.tech/project/searxng-search) [![Downloads](https://static.pepy.tech/badge/searxng-search/week)](https://pepy.tech/project/searxng-search)
# searxng_search<a name="TOP"></a>

Web search using the searxng instances.

## Table of Contents
* [Install](#install)
* [SearxngSearch class](#searxngsearch-class)
  * [Proxy](#proxy)
  * [Exceptions](#exceptions)
  * [search()](#search)

___
## Install
```python
pip install -U searxng_search
```
___
## SearxngSearch class
```python3
"""Searxng search. Query params: https://docs.searxng.org/dev/search_api.html.

Args:
    q: search query.
    language: code of the language. Defaults to "auto".
    pageno: search page number. Defaults to 1.
    time_range: "day", "week", "month", "year". Defaults to "".
    safesearch: 0, 1, 2. Defaults to 1.
"""
```

Here is an example of initializing the SeaxngSearch class.
```python3
from searxng_search import SearxngSearch

results = SearxngSearch().search("python")
print(results)
```
___
### Proxy

Package supports http/https/socks proxies. Example: `http://user:pass@example.com:3128`.
Use a rotating proxy. Otherwise, use a new proxy with each SearxngSearch class initialization.

*1. The easiest way. Launch the Tor Browser*
```python3
from searxng_search import SearxngSearch

ss = SearxngSearch(proxy="socks5://127.0.0.1:9150", timeout=20)
results = SS.search("python")
```
*2. Use any proxy server* (*example with [iproyal rotating residential proxies](https://iproyal.com?r=residential_proxies)*)
```python3
from searxng_search import SearxngSearch

ss = SearxngSearch(proxy="socks5h://user:password@geo.iproyal.com:32325", timeout=20)
results = ss.text("something you need")
```
___
### Exceptions

Exceptions:
- `SearxngSearchException`: Base exception for searxng_search errors.
- `RatelimitException`: Inherits from SearxngSearchException, raised for exceeding request rate limits.
- `TimeoutException`: Inherits from SearxngSearchException, raised for request timeouts.
___
### search()

```python
def search(
    self,
    q: str,
    language: str = "auto",
    pageno: str | int = 1,
    time_range: str = "",
    safesearch: str | int = 1,
) -> list[dict[str, str]]:
    """Searxng search. Query params: https://docs.searxng.org/dev/search_api.html.

    Args:
        q: search query.
        language: code of the language. Defaults to "auto".
        pageno: search page number. Defaults to 1.
        time_range: "day", "week", "month", "year". Defaults to "".
        safesearch: 0, 1, 2. Defaults to 1.

    Returns:
        List of dictionaries with search results.
```
***Example***
```python
from searxng_search import SS  # SS = SearxngSearch (alias)

results = SS().search("python", language="fr", pageno=4, time_range="year", safesearch=0)
print(results)
```
