from sqlalchemy.orm import Session
from models.expenses_model import  Expense
from models.categoreies_models import Category
from schemas.expense_schemas import ExpenseCreate, ExpenseUpdate
from sqlalchemy import func, extract

def create_expense(db: Session, data: ExpenseCreate):
    expense = Expense(**data.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def update_expense(db: Session, expense_id: int, data: ExpenseUpdate):
    expense = get_expense(db, expense_id)
    if not expense:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense_id: int):
    expense = get_expense(db, expense_id)
    if not expense:
        return None
    db.delete(expense)
    db.commit()
    return expense

# Filtering
def list_expenses(db: Session, category_id=None, min_amount=None, max_amount=None,
                  from_date=None, to_date=None):

    query = db.query(Expense)

    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if min_amount:
        query = query.filter(Expense.amount >= min_amount)
    if max_amount:
        query = query.filter(Expense.amount <= max_amount)
    if from_date:
        query = query.filter(Expense.expense_date >= from_date)
    if to_date:
        query = query.filter(Expense.expense_date <= to_date)

    return query.all()

# Monthly summary
def monthly_summary(db: Session, year: int, month: int):
    q = db.query(
        Category.name,
        func.sum(Expense.amount)
    ).join(Category, Expense.category_id == Category.id)\
     .filter(extract('year', Expense.expense_date) == year,
            extract('month', Expense.expense_date) == month)\
     .group_by(Category.name)

    breakdown = {name: total for name, total in q.all()}

    total_expense = sum(breakdown.values()) if breakdown else 0

    return {
        "year": year,
        "month": month,
        "total_expense": total_expense,
        "category_breakdown": breakdown
    }

# Top categories
def top_categories(db: Session, limit: int):
    q = db.query(
        Category.name,
        func.sum(Expense.amount).label("total")
    ).join(Category, Expense.category_id == Category.id)\
     .group_by(Category.name)\
     .order_by(func.sum(Expense.amount).desc())\
     .limit(limit)

    return [{"category": name, "total": total} for name, total in q.all()]