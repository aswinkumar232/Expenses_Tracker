from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from logic.database import get_db
from datetime import date
from services.expense_service import create_expense, get_expense, update_expense, delete_expense, list_expenses, monthly_summary, top_categories
from schemas.expense_schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate


expense_router = APIRouter(prefix="/expenses", tags=["Expenses"])

@expense_router.post("/", response_model=ExpenseOut)
def create(data: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense(db, data)

@expense_router.get("/", response_model=list[ExpenseOut])
def list_expenses_route(
    category_id: int | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db)
):
    return list_expenses(db, category_id, min_amount, max_amount, from_date, to_date)

@expense_router.get("/summary/monthly")
def monthly_summary_route(year: int, month: int, db: Session = Depends(get_db)):
    return monthly_summary(db, year, month)

@expense_router.get("/top-categories")
def top_categories_route(limit: int = 3, db: Session = Depends(get_db)):
    return top_categories(db, limit)


@expense_router.get("/{id}", response_model=ExpenseOut)
def get(id: int, db: Session = Depends(get_db)):
    expense = get_expense(db, id)
    if not expense:
        raise HTTPException(404, "Expense not found")
    return expense

@expense_router.put("/{id}", response_model=ExpenseOut)
def update(id: int, data: ExpenseUpdate, db: Session = Depends(get_db)):
    updated = update_expense(db, id, data)
    if not updated:
        raise HTTPException(404, "Expense not found")
    return updated

@expense_router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = delete_expense(db, id)
    if not deleted:
        raise HTTPException(404, "Expense not found")
    return {"detail": "Expense deleted"}


