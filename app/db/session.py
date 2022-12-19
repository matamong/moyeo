from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings.app import AppSettings

engine = create_engine(AppSettings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)