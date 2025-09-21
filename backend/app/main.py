from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base
from .routers import expenses

app = FastAPI(title="Expense Intellect API")

# Database setup (SQLite for dev)
engine = create_engine("sqlite:///./expenses.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(expenses.router)