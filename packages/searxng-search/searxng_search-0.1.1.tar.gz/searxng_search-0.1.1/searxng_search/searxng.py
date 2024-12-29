from __future__ import annotations

import logging
import os
from functools import cached_property
from pathlib import Path
from random import choice
from time import time
from types import TracebackType
from typing import cast

import primp  # type: ignore
from lxml.etree import _Element
from lxml.html import HTMLParser as LHTMLParser
from lxml.html import document_fromstring

from .exceptions import RatelimitException, SearxngSearchException, TimeoutException

logger = logging.getLogger("SearxngSearch")


class SearxngSearch:
    """Searxng search class to get search results searxng instances"""

    _impersonates = (
        "chrome_100", "chrome_101", "chrome_104", "chrome_105", "chrome_106", "chrome_107",
        "chrome_108", "chrome_109", "chrome_114", "chrome_116", "chrome_117", "chrome_118",
        "chrome_119", "chrome_120", "chrome_123", "chrome_124", "chrome_126", "chrome_127",
        "chrome_128", "chrome_129", "chrome_130", "chrome_131",
        "safari_ios_16.5", "safari_ios_17.2", "safari_ios_17.4.1", "safari_ios_18.1.1",
        "safari_15.3", "safari_15.5", "safari_15.6.1", "safari_16", "safari_16.5",
        "safari_17.0", "safari_17.2.1", "safari_17.4.1", "safari_17.5",
        "safari_18", "safari_18.2",
        "safari_ipad_18",
        "edge_101", "edge_122", "edge_127", "edge_131",
        "firefox_109", "firefox_133",
    )  # fmt: skip
    _searxng_proxy: str | None = os.environ.get("SEARXNG_PROXY")
    _searxng_file = Path.home() / "searxng_instances.txt"

    def __init__(
        self,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        timeout: int | None = 15,
        verify: bool = True,
    ) -> None:
        """Initialize the SearxngSearch object.

        Args:
            headers (dict, optional): Dictionary of headers for the HTTP client. Defaults to None.
            proxy (str, optional): proxy for the HTTP client, supports http/https/socks5 protocols.
                example: "http://user:pass@example.com:3128". Defaults to None.
            timeout (int, optional): Timeout value for the HTTP client. Defaults to 10.
            verify (bool): SSL verification when making the request. Defaults to True.
        """
        self.proxy: str | None = self._searxng_proxy or proxy
        self.headers = headers or {}
        self.impersonate = choice(self._impersonates)
        self.client = primp.Client(
            headers=self.headers,
            proxy=self.proxy,
            timeout=timeout,
            impersonate=self.impersonate,
            follow_redirects=True,
            verify=verify,
        )
        self.searxng_instances = self._load_searxng_instances()
        self.searxng_instance = choice(self.searxng_instances)

    def __enter__(self) -> SearxngSearch:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        pass

    @cached_property
    def parser(self) -> LHTMLParser:
        """Get HTML parser."""
        return LHTMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True, collect_ids=False)

    def _get_url(
        self,
        method: str,
        url: str,
        params: dict[str, str] | None = None,
    ) -> bytes:
        try:
            resp = self.client.request(method, url, params=params)
        except Exception as ex:
            if "time" in str(ex).lower():
                raise TimeoutException(f"{url} {type(ex).__name__}: {ex}") from ex
            raise SearxngSearchException(f"{url} {type(ex).__name__}: {ex}") from ex
        if resp.status_code == 200:
            return cast(bytes, resp.content)
        elif resp.status_code == 429:
            raise RatelimitException(f"{resp.url} {resp.status_code} Ratelimit")
        raise SearxngSearchException(f"{resp.url} return None. {params=}")

    def _get_searxng_instances(self) -> list[str]:
        url = "https://searx.space/data/instances.json"
        resp = primp.Client(
            impersonate=self.impersonate,
            proxy=self.proxy,
        ).get(url)
        data = resp.json()
        instances = data.get("instances")
        results = []
        for k, v in instances.items():
            if (
                v["network_type"] == "normal"
                and v["http"]["status_code"] == 200
                and (v["engines"].get("bing") or v["engines"].get("google"))
                and (v.get("timing", {}).get("initial", {}).get("success_percentage") == 100)
                and (v.get("timing", {}).get("search", {}).get("success_percentage") == 100)
                and (v.get("timing", {}).get("search", {}).get("all", {}).get("median") <= 1)
                and (v.get("timing", {}).get("search_go", {}).get("success_percentage") == 100)
            ):
                results.append(f"{k}search")
        return results

    def _load_searxng_instances(self) -> list[str]:
        data = []
        if self._searxng_file.exists() and time() - self._searxng_file.stat().st_mtime < 3600:
            with open(self._searxng_file) as file:
                data = file.read().split()
        elif not data:
            data = self._get_searxng_instances()
            with open(self._searxng_file, "w", encoding="utf-8") as file:
                file.write("\n".join(data))
        return data

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

        Raises:
            SearxngSearchException: Base exception for searxng_search errors.
            RatelimitException: Inherits from SearxngSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from SearxngSearchException, raised for API request timeouts.
        """
        assert q, "q is mandatory"

        payload = {
            "q": q,
            "category_general": "1",
            "pageno": f"{pageno}",
            "language": language,
            "time_range": time_range,
            "safesearch": f"{safesearch}",
            "theme": "simple",
        }

        results: list[dict[str, str]] = []

        resp_content = self._get_url("POST", self.searxng_instance, params=payload)
        if b"No results were found" in resp_content:
            return results

        tree = document_fromstring(resp_content, self.parser)

        tokenxpath = tree.xpath("//head//link[contains(@href, '/client')]/@href")
        token = str(tokenxpath[0]).lstrip("/searxng") if isinstance(tokenxpath, list) else None
        if token:
            primp.Client(
                impersonate=self.impersonate,
                proxy=self.proxy,
            ).post(
                f"{self.searxng_instance.rstrip('search')}{token}",
            )

        elements = tree.xpath("//div[@role='main']//article")
        if not isinstance(elements, list):
            return results

        for e in elements:
            if isinstance(e, _Element):
                hrefxpath = e.xpath(".//h3/a/@href")
                href = str(hrefxpath[0]) if hrefxpath and isinstance(hrefxpath, list) else None
                if href:
                    titlexpath = e.xpath(".//h3//text()")
                    title = (
                        str("".join(str(x) for x in titlexpath)) if titlexpath and isinstance(titlexpath, list) else ""
                    )
                    bodyxpath = e.xpath(".//p//text()")
                    body = "".join(str(x) for x in bodyxpath) if bodyxpath and isinstance(bodyxpath, list) else ""
                    results.append(
                        {
                            "title": title,
                            "href": href,
                            "body": body.strip(),
                        }
                    )

        return results
