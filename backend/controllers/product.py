from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select, text
from models import Product, ProductCreate, ProductUpdate
from unicodedata import normalize, combining


class ProductController():

    @classmethod
    def index(self, id: int, db: Session) -> Product:
        obj = db.get(Product, id)
        if not obj:
            raise HTTPException(
                status_code=404, detail=f"Product not found with id {id}.")
        return obj

    @classmethod
    def show(self, query: str, db: Session) -> List[Product]:
        if query:
            statement = text("SELECT * FROM product p WHERE UNACCENT(LOWER(p.name)) LIKE '%' || :name || '%'")
            results = db.exec(statement, params={"name": normalize('NFD', u"".join([c for c in normalize('NFKD', query) if not combining(c)]).lower())}).all()
        else:
            results = db.exec(select(Product)).all()
        return results

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
