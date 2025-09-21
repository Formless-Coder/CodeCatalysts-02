from sqlalchemy.orm import Session
from ..database import Policy

def get_policies(db: Session):
    return db.query(Policy).all()

def apply_policies(expense, policies):
    flagged = False
    for policy in policies:
        for rule in policy.rules:
            if rule['type'] == 'amount_max' and expense.amount > rule['value']:
                flagged = True
            # Add more rule types (e.g., 'category_block': if expense.category in rule['values'])
    return flagged