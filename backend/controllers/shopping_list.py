from typing import List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from db import get_session
from models import ProductShoppingList, ProductShoppingListBase, ProductShoppingListCreate, ShoppingList, ShoppingListRead, ShoppingListCreate, ShoppingListUpdate


class ShoppingListController():

    @classmethod
    def index(self, id: int, db: Session = Depends(get_session)) -> ShoppingList:
        obj = db.get(ShoppingList, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Shopping list not found with id {id}.")
        return obj

    @classmethod
    def index_product(self, id: int, product_id: int, db: Session = Depends(get_session)) -> ShoppingList:
        statement = select(ProductShoppingList).where(ProductShoppingList.shopping_list_id == id, ProductShoppingList.product_id == product_id)
        try:
            product_shopping_list = db.exec(statement).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found in shopping list with id {id}.")
        return product_shopping_list


    @classmethod
    def show(self, db: Session = Depends(get_session)) -> List[ShoppingList]:
        statement = select(ShoppingList)
        results = db.exec(statement).all()
        return results

    
    @classmethod
    def store(self, data: ShoppingListCreate, db: Session = Depends(get_session)) -> ShoppingList:
        shopping_list = ShoppingList.from_orm(data)
        db.add(shopping_list)
        db.commit()
        db.refresh(shopping_list)
        return shopping_list


    @classmethod
    def store_product(self, id: int, data: ProductShoppingListCreate, db: Session = Depends(get_session)):
        shopping_list = db.get(ShoppingList, id)
        product = ProductShoppingList.from_orm(data)
        shopping_list.products.append(product)
        db.add(shopping_list)
        db.commit()
        db.refresh(shopping_list)
        return shopping_list


    @classmethod
    def update(self, id: int, data: ShoppingListUpdate, db: Session = Depends(get_session)) -> ShoppingList:
        shopping_list = db.get(ShoppingList, id)
        if not shopping_list:
            raise HTTPException(status_code=404, detail=f"Shopping list not found with id {id}.")
        data_dict = data.dict(exclude_unset=True)
        data_dict.pop('products', None)
        for k, v in data_dict.items():
            setattr(shopping_list, k, v)
        db.add(shopping_list)
        db.commit()
        db.refresh(shopping_list)
        return shopping_list

    
    @classmethod
    def update_product(self, id: int, product_id: int, product: ProductShoppingListBase, db: Session = Depends(get_session)):
        statement = select(ProductShoppingList).where(ProductShoppingList.shopping_list_id == id, ProductShoppingList.product_id == product_id)
        try:
            product_shopping_list = db.exec(statement).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found in shopping list with id {id}.")
        data_dict = product.dict(exclude_unset=True)
        for k, v in data_dict.items():
            setattr(product_shopping_list, k, v)
        db.add(product_shopping_list)
        db.commit()
        db.refresh(product_shopping_list)
        return product_shopping_list
        

    @classmethod
    def destroy(self, id: int, db: Session = Depends(get_session)) -> None:
        obj = db.get(ShoppingList, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Shopping list not found with id {id}.")
        db.delete(obj)
        db.commit()

    @classmethod
    def destroy_product(self, id: int, product_id: int, db: Session = Depends(get_session)):
        statement = select(ProductShoppingList).where(ProductShoppingList.shopping_list_id == id, ProductShoppingList.product_id == product_id)
        try:
            product_shopping_list = db.exec(statement).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found in shopping list with id {id}.")
        db.delete(product_shopping_list)
        db.commit()