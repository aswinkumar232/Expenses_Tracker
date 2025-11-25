from sqlalchemy import Column, Integer, String,Float, ForeignKey, Date, DateTime, func
from logic.database import Base
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    expense_date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("Category")