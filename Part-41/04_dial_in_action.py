"""
Part 41 · File 04 — The Dial in Action (replace print() with logging)
Notes section: "The Dial in Action — Replace print() with logging"

The debug lines stay in the code FOREVER — the dial decides if they show:
  - LOG_LEVEL=DEBUG  → you see the debug detail (development)
  - LOG_LEVEL=INFO   → debug is silently skipped (production)

No code changes, no deleting prints — just turn the dial.

Run it:
    python 04_dial_in_action.py
Then flip LOG_LEVEL in .env between INFO and DEBUG and run again.
"""

import logging
import os
from pathlib import Path

try:
    from dotenv import load_dotenv          # pip install python-dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),    # the dial — read from .env
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def calculate_total(items):
    logger.debug(f"items received: {items}")     # shown only when the dial = DEBUG
    total = sum(i["price"] * i["quantity"] for i in items)
    logger.info(f"calculated total: {total}")    # shown in production too (INFO)
    return total


cart = [
    {"name": "book", "price": 300, "quantity": 2},
    {"name": "pen", "price": 20, "quantity": 5},
]
calculate_total(cart)
