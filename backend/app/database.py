from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    vendor = Column(String)
    category = Column(String)
    amount = Column(Float)
    status = Column(String, default="Pending")
    flagged = Column(Boolean, default=False)
    data_hash = Column(String)  # For duplicate detection

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rules = Column(JSON)  # e.g., [{"type": "amount_max", "value": 200, "action": "flag"}]