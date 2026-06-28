"""
Part 41 — import module_logger to watch __name__ become the module name.

Run this file directly:
    uv run main.py

main.py's own __name__ is "__main__", but the file it IMPORTS (module_logger)
reports __name__ == "module_logger" — that is the whole lesson of File 03.
"""

import logging
import module_logger   # importing RUNS module_logger.py; inside it, __name__ == "module_logger"

logger = logging.getLogger(__name__)   # here __name__ == "__main__"
logger.info(f"main speaking — my __name__ is '{__name__}'")
logger.info(f"the module I imported reports __name__ = '{module_logger.__name__}'")
