from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from logic.database import get_db
from schemas.categories_schemas import CategoryCreate, CategoryOut, CategoryUpdate
from services.categories_service import create_category, get_categories, get_category, update_category, delete_category

category_router = APIRouter(prefix="/categories", tags=["Categories"])

@category_router.post("/", response_model=CategoryOut)
def create(data: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, data)

@category_router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@category_router.get("/{id}", response_model=CategoryOut)
def get(id: int, db: Session = Depends(get_db)):
    category = get_category(db, id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category

@category_router.put("/{id}", response_model=CategoryOut)
def update(id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    updated = update_category(db, id, data)
    if not updated:
        raise HTTPException(404, "Category not found")
    return updated

@category_router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = delete_category(db, id)
    if not deleted:
        raise HTTPException(404, "Category not found")
    return {"detail": "Category deleted"}

