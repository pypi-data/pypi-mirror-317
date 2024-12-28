from searxng_search import SS, SearxngSearch


def test_context_manager() -> None:
    with SearxngSearch() as sxs:
        results = sxs.search("cars", pageno=2)
        assert len(results) >= 5


def test_text_html() -> None:
    results = SS().search("eagle", safesearch=0, language="br", time_range="year", pageno=2)
    assert len(results) >= 5
