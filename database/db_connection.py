import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Default to SQLite for local development if no DATABASE_URL is provided
db_file = DATA_DIR / "youtube_analytics.db"
db_path = db_file.resolve().as_posix()
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

# Log the connection attempt for debugging
logger.info(f"Connecting to database at: {DATABASE_URL}")

# Create engine with SQLite multi-threading support if applicable
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
