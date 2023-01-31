from fastapi import APIRouter, status, Depends
from typing import List

from sqlmodel import Session
from controllers.auth import get_current_user
from db import get_session

from models import ShoppingListRead, ShoppingListCreate, ShoppingListUpdate, User
from models import ProductShoppingListRead, ProductShoppingListCreate, ProductShoppingListUpdate
from controllers import ShoppingListController

router = APIRouter( prefix="/shopping-lists", tags=["shopping-lists"])

@router.get("", response_model=List[ShoppingListRead])
async def fetch_shopping_lists(user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.show(user, db)

@router.get("/{id}", response_model=ShoppingListRead)
async def fetch_shopping_list(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.index(id, user, db)

@router.get("/{id}/product/{product_id}", response_model=ProductShoppingListRead, responses={404: {"description": "The item was not found"}})
async def fetch_shopping_list(id: int, product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.index_product(id, product_id, user, db)

@router.post("", response_model=ShoppingListRead, status_code=status.HTTP_201_CREATED)
async def create_shopping_list(shopping_list: ShoppingListCreate, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.store(shopping_list, user, db)

@router.post("/{id}/product", response_model=ProductShoppingListRead, status_code=status.HTTP_201_CREATED)
async def create_product_shopping_list(id: int, data: ProductShoppingListCreate, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.store_product(id, data, user, db)

@router.patch("/{id}", response_model=ShoppingListRead)
async def update_shopping_list(id: int, shopping_list: ShoppingListUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.update(id, shopping_list, user, db)

@router.patch("/{id}/product/{product_id}", response_model=ProductShoppingListRead)
async def update_shopping_list_product(id: int, product_id: int, product: ProductShoppingListUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.update_product(id, product_id, product, user, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_shopping_list(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.destroy(id, user, db)

@router.delete("/{id}/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_shopping_list_product(id: int, product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    return ShoppingListController.destroy_product(id, product_id, user, db)