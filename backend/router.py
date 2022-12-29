from fastapi import APIRouter, Depends

from routes import auth, products, shopping_lists
from controllers.auth import get_current_user

auth_router = APIRouter()

auth_router.include_router(auth.router)

data_router = APIRouter(dependencies=[Depends(get_current_user)])

data_router.include_router(products.router)
data_router.include_router(shopping_lists.router)