import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
import joblib
import hashlib

# Load trained model
MODEL_PATH = '../../models/anomaly_model.pkl'
anomaly_model = joblib.load(MODEL_PATH)

def compute_hash(expense):
    hash_str = f"{expense.date}_{expense.vendor}_{expense.amount}"
    return hashlib.md5(hash_str.encode()).hexdigest()

def detect_anomalies(db: Session):
    from ..database import Expense
    expenses = db.query(Expense).all()
    if not expenses:
        return []
    df = pd.DataFrame([{
        'id': e.id,
        'amount': e.amount,
        'data_hash': e.data_hash
    } for e in expenses])
    # ML anomalies
    preds = anomaly_model.predict(df[['amount']])
    ml_flagged = df[preds == -1]['id'].tolist()
    # Duplicate detection
    dupe_groups = df.groupby('data_hash').filter(lambda x: len(x) > 1)
    dupe_flagged = dupe_groups['id'].tolist()
    return list(set(ml_flagged + dupe_flagged))