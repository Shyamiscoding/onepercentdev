"""
Part 41 · File 07 — Send your logs to a Grafana dashboard (Grafana Cloud + Loki)
Notes section: "See Your Logs in a Grafana Dashboard"

Here the APP pushes its own logs straight to Loki using one extra handler — the
same addHandler pattern from Files 05/06. (In production a separate agent like
Promtail / Grafana Alloy does the delivery instead — see notes.md.)

Run it:
    python 07_grafana_loki.py
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
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

LOKI_URL = os.getenv("LOKI_URL")
LOKI_USER = os.getenv("LOKI_USER")
LOKI_TOKEN = os.getenv("LOKI_TOKEN")

if LOKI_URL and LOKI_USER and LOKI_TOKEN:
    import logging_loki

    # The library tags the level as "severity"; Grafana color-codes on "level".
    logging_loki.emitter.LokiEmitter.level_tag = "level"

    loki = logging_loki.LokiHandler(
        url=LOKI_URL,                       # https://logs-prod-XXX.grafana.net/loki/api/v1/push
        tags={"app": "part41"},             # query later with {app="part41"}
        auth=(LOKI_USER, LOKI_TOKEN),       # (numeric User, access-policy token)
        version="1",
    )
    logger.addHandler(loki)
    logger.info("Loki handler attached — these logs are also going to Grafana Cloud")
else:
    logger.warning("LOKI_* not set in .env — logging to console only (see steps above)")

logger.info("part 41 — logging demo started")
logger.warning("this warning will also show up in Grafana")
logger.error('and this error — search {app="part41"} in Grafana to find it')

print("done — if you added the Loki handler, open your Grafana dashboard to see these lines")
