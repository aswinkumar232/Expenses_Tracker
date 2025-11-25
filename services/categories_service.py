from sqlalchemy.orm import Session
from models.categoreies_models import Category
from schemas.categories_schemas import CategoryCreate, CategoryUpdate
from sqlalchemy import func

def create_category(db: Session, data: CategoryCreate):
    category = Category(**data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.query(Category).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = get_category(db, category_id)
    if not category:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category



