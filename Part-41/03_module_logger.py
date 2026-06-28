"""
Part 41 · File 03 — Module-Level Loggers (getLogger(__name__))
Notes section: "Module-Level Loggers (the pro pattern)"
Real projects give every file its OWN logger, named after the module, so each
log line shows WHICH file produced it. The name comes from __name__:
  - run the file directly → __name__ is "__main__"
  - import the file       → __name__ is the module name (e.g. "utils")
Run it:
    python 03_module_logger.py
Watch the name between the dashes: the named logger shows "__main__",
while a direct logging.info() call shows "root".
"""
import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)                              # keep all logs in Part-41/logs/

logging.basicConfig(
    level=logging.INFO,                                   # the dial — show INFO and above
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
    filename=LOG_DIR / "app_basic.log",                   # omit this line → logs to the console instead
    filemode="a",                                         # "a" = append (default) · "w" = overwrite each run
    encoding="utf-8",
)

# The pro pattern: one named logger per file
logger = logging.getLogger(__name__)    # name = "__main__" when this file is run directly
logger.info("named logger — the name between the dashes is __name__ (here: __main__)")
# Compare: calling logging.info() directly uses the single shared ROOT logger
logging.info("root logger — calling logging.info() directly shows 'root' instead")
# print(__name__,'__name__')
