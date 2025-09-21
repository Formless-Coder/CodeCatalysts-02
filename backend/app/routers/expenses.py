from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ...database import SessionLocal, Expense, Policy
from ...models import ExpenseCreate, ExpenseOut, PolicyCreate, PolicyOut
from ...utils.ocr import extract_text
from ...utils.categorize import categorize
from ...utils.anomaly import detect_anomalies, compute_hash
from ...utils.policy import apply_policies

router = APIRouter(prefix="/expenses", tags=["expenses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-receipt/", response_model=ExpenseOut)
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    import time
    start_time = time.time()  # For KPI: processing time
    contents = await file.read()
    extracted = extract_text(contents)
    category = categorize(extracted['raw_text'])
    create_data = ExpenseCreate(**extracted, category=category)
    new_expense = Expense(**create_data.dict(), data_hash=compute_hash(create_data))
    policies = db.query(Policy).all()
    new_expense.flagged = apply_policies(new_expense, policies)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    flagged = detect_anomalies(db)
    if new_expense.id in flagged:
        new_expense.flagged = True
        db.commit()
    process_time = time.time() - start_time
    print(f"Processing time: {process_time} seconds")  # Log for KPIs
    return new_expense

@router.get("/", response_model=list[ExpenseOut])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.post("/policies/", response_model=PolicyOut)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    new_policy = Policy(**policy.dict())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy

@router.get("/policies/", response_model=list[PolicyOut])
def get_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()