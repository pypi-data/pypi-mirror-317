class SearxngSearchException(Exception):
    """Base exception class for searxng_search."""


class RatelimitException(SearxngSearchException):
    """Raised for rate limit exceeded errors during API requests."""


class TimeoutException(SearxngSearchException):
    """Raised for timeout errors during API requests."""
