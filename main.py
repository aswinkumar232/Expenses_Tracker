from fastapi import FastAPI
from logic.database import Base, engine
from routers.categories_router import  category_router
from routers.expense_router import expense_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(category_router)
app.include_router(expense_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Expense Tracker API"}

