import logging

from .searxng import SearxngSearch
from .version import __version__

SS = SearxngSearch
__all__ = ["SearxngSearch", "SS", "__version__"]


# A do-nothing logging handler
# https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("searxng_search").addHandler(logging.NullHandler())
