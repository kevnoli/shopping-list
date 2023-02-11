from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlmodel import Session, col, select, text
from sqlalchemy import func
from models import Product, ProductCreate, ProductShoppingList, ProductUpdate
from unicodedata import normalize, combining
from sqlalchemy.sql.functions import ReturnTypeFromArgs

class unaccent(ReturnTypeFromArgs):
    pass


class ProductController():

    @classmethod
    def index(self, id: int, db: Session) -> Product:
        obj = db.get(Product, id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"Product not found with id {id}.")
        return obj

    @classmethod
    def show(self, query: str, exclude: int, db: Session) -> List[Product]:
        statement = select(Product)
        if exclude:
            exclude_statement = select(ProductShoppingList.product_id).where(ProductShoppingList.shopping_list_id == exclude)
            statement = statement.where(col(Product.id).not_in(exclude_statement))

        if query:
            normalizedQuery = normalize('NFD', u"".join([c for c in normalize('NFKD', query) if not combining(c)]).lower())
            statement = statement.where(unaccent(func.lower(Product.name)).like(f"%{normalizedQuery}%"))

        return db.exec(statement).all()

    @classmethod
    def store(self, data: ProductCreate, db: Session) -> Product:
        product = Product.from_orm(data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @classmethod
    def update(self, id: int, data: ProductUpdate, db: Session) -> Product:
        product = db.get(Product, id)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product not found with id {id}.")
        data_dict = data.dict(exclude_unset=True)
        data_dict["updated_at"] = datetime.utcnow()
        for k, v in data_dict.items():
            setattr(product, k, v)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @classmethod
    def destroy(self, id: int, db: Session) -> None:
        obj = db.get(Product, id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"Product not found with id {id}.")
        db.delete(obj)
        db.commit()
