from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    date: str
    vendor: str
    category: str
    amount: float

class ExpenseOut(ExpenseCreate):
    id: int
    status: str
    flagged: bool

class PolicyCreate(BaseModel):
    name: str
    rules: list[dict]  # e.g., [{"type": "amount_max", "value": 200}]

class PolicyOut(PolicyCreate):
    id: int