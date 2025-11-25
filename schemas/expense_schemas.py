from pydantic import BaseModel, Field
from datetime import date, datetime


class ExpenseBase(BaseModel):
    title: str
    amount: float = Field(..., gt=0)
    category_id: int
    expense_date: date
    notes: str | None = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: float | None = Field(None, gt=0)
    category_id: int | None = None
    expense_date: date | None = None
    notes: str | None = None

class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
