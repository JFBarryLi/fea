import logging
from rich.logging import RichHandler

logging.basicConfig(
    format='%(levelname)s | %(name)s | %(message)s',
    level=logging.INFO,
    handlers=[RichHandler(rich_tracebacks=True)],
)
