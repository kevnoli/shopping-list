from fastapi import APIRouter, Depends

from routes import auth, products, shopping_lists
from controllers.auth import oauth2_scheme

auth_router = APIRouter()

auth_router.include_router(auth.router)

data_router = APIRouter(dependencies=[Depends(oauth2_scheme)])

data_router.include_router(products.router)
data_router.include_router(shopping_lists.router)