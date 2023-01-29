from fastapi import APIRouter, status, Depends
from typing import List
from db import get_session

from models import ProductRead, ProductCreate, ProductUpdate
from controllers import ProductController

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[ProductRead])
async def fetch_products(query: str = None, db = Depends(get_session)):
    return ProductController.show(query, db)

@router.get("/{id}", response_model=ProductRead)
async def fetch_product(id: int, db = Depends(get_session)):
    return ProductController.index(id, db)

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db = Depends(get_session)):
    return ProductController.store(product, db)

@router.patch("/{id}", response_model=ProductRead)
async def update_product(id: int, product: ProductUpdate, db = Depends(get_session)):
    return ProductController.update(id, product, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_product(id: int, db = Depends(get_session)):
    return ProductController.destroy(id, db)