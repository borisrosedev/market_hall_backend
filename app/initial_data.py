import logging
from sqlmodel import Session
from app.core.db import init_db
from app.core.config import settings
from sqlmodel import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True, future=True)

def main() -> None:
    logger.info("Creating initial data")
    with Session(engine) as session:
        init_db(session)  # create super user and data (idempotent)
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
