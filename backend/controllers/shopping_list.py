from datetime import datetime
from typing import List
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from db import get_session
from models import ProductShoppingList, ProductShoppingListBase, ProductShoppingListCreate, ShoppingList, ShoppingListCreate, ShoppingListRead, ShoppingListUpdate, User, UserShoppingList


class ShoppingListController():

    @classmethod
    def index(self, id: int, user: User, db: Session) -> ShoppingList:
        try:
            shopping_list = db.exec(
                select(ShoppingList)
                .join(UserShoppingList)
                .where(ShoppingList.id == id, UserShoppingList.user == user)
            ).one()
            return shopping_list
        except:
            raise HTTPException(
                status_code=404, detail=f"Shopping list not found with id {id}.")

    @classmethod
    def index_product(self, id: int, product_id: int, user: User, db: Session) -> ShoppingList:
        try:
            product_shopping_list = db.exec(
                select(ProductShoppingList)
                .join(ShoppingList)
                .join(UserShoppingList)
                .where(
                    ProductShoppingList.shopping_list_id == id,
                    ProductShoppingList.product_id == product_id,
                    UserShoppingList.user == user)
            ).one()
            return product_shopping_list
        except:
            raise HTTPException(
                status_code=404, detail=f"Product with id {product_id} not found in shopping list with id {id}.")

    @classmethod
    def show(self, user: User, db: Session) -> List[ShoppingList]:
        results = db.exec(
            select(ShoppingList)
            .join(UserShoppingList)
            .where(UserShoppingList.user == user)
        ).all()
        return results

    @classmethod
    def store(self, data: ShoppingListCreate, user: User, db: Session) -> ShoppingList:
        shopping_list = ShoppingList.from_orm(data)
        db.add(shopping_list)
        user_link = UserShoppingList(
            shopping_list=shopping_list, user=user, owner=True)
        db.add(user_link)
        db.commit()
        db.refresh(shopping_list)
        return shopping_list

    @classmethod
    def store_product(self, id: int, data: ProductShoppingListCreate, user: User, db: Session):
        shopping_list = self.index(id, user, db)
        data.shopping_list_id = shopping_list.id
        product = ProductShoppingList.from_orm(data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @classmethod
    def update(self, id: int, data: ShoppingListUpdate, user: User, db: Session) -> ShoppingList:
        shopping_list = self.index(id, user, db)
        data_dict = data.dict(exclude_unset=True)
        data_dict["updated_at"] = datetime.utcnow()
        for k, v in data_dict.items():
            setattr(shopping_list, k, v)
        db.add(shopping_list)
        db.commit()
        db.refresh(shopping_list)
        return shopping_list

    @classmethod
    def update_product(self, id: int, product_id: int, product: ProductShoppingListBase, user: User, db: Session):
        product_shopping_list = self.index_product(id, product_id, user, db)
        data_dict = product.dict(exclude_unset=True)
        data_dict["updated_at"] = datetime.utcnow()
        for k, v in data_dict.items():
            setattr(product_shopping_list, k, v)
        db.add(product_shopping_list)
        db.commit()
        db.refresh(product_shopping_list)
        return product_shopping_list

    @classmethod
    def destroy(self, id: int, user: User, db: Session) -> None:
        shopping_list = self.index(id, user, db)
        db.delete(shopping_list)
        db.commit()

    @classmethod
    def destroy_product(self, id: int, product_id: int, user: User, db: Session):
        product_shopping_list = self.index_product(id, product_id, user, db)
        db.delete(product_shopping_list)
        db.commit()
