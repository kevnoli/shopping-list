from typing import List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Product, ProductCreate, ProductUpdate

class ProductController():

    @classmethod
    def index(self, id: int, db: Session = Depends(get_session)) -> Product:
        obj = db.get(Product, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Product not found with id {id}.")
        return obj


    @classmethod
    def show(self, db: Session = Depends(get_session)) -> List[Product]:
        statement = select(Product)
        results = db.exec(statement).all()
        return results

    
    @classmethod
    def store(self, data: ProductCreate, db: Session = Depends(get_session)) -> Product:
        product = Product.from_orm(data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product


    @classmethod
    def update(self, id: int, data: ProductUpdate, db: Session = Depends(get_session)) -> Product:
        product = db.get(Product, id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found with id {id}.")
        data_dict = data.dict(exclude_unset=True)
        for k, v in data_dict.items():
            setattr(product, k, v)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
        

    @classmethod
    def destroy(self, id: int, db: Session = Depends(get_session)) -> None:
        obj = db.get(Product, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Product not found with id {id}.")
        db.delete(obj)
        db.commit()

