# app/backend_pre_start.py
from __future__ import annotations

import logging
from sqlalchemy import text
from sqlmodel import create_engine
from tenacity import retry, wait_fixed, stop_after_attempt, before_log, after_log

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_TRIES = 60 * 5   # 5 minutes
WAIT_SECONDS = 1     # 1s entre tentatives

# Engine local uniquement pour le ping
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    pool_pre_ping=True,
    future=True,
)

@retry(
    stop=stop_after_attempt(MAX_TRIES),
    wait=wait_fixed(WAIT_SECONDS),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
)
def wait_for_db() -> None:
    """wait for the db to answer with SELECT 1 (w/ retry)."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

def main() -> None:
    logger.info("Waiting for database to be ready…")
    wait_for_db()
    logger.info("Database is ready.")

if __name__ == "__main__":
    main()
