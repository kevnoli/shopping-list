from pydantic import condecimal
from sqlmodel import Column, ForeignKey, Integer, Relationship, SQLModel, Field
from typing import Optional, List
from datetime import datetime

# AccessToken
class AccessToken(SQLModel):
    access_token: str
    token_type: str
    refresh_token: str

# User
class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=16, nullable=False)
    email: str = Field(unique=True, max_length=320, nullable=False)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    password: str = Field(max_length=255, nullable=False)

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    password: str
    repeat_password: str

class UserUpdate(UserBase):
    pass

# Product-ShoppingList association table 
class ProductShoppingListBase(SQLModel):
    price: condecimal(max_digits=10, decimal_places=2, gt=0) = Field(default=0, nullable=True)
    amount_to_buy: int | None = Field(default=None, nullable=True)
    amount_bought: int | None = Field(default=None, nullable=True)

class ProductShoppingList(ProductShoppingListBase, table=True):
    shopping_list_id: int = Field(primary_key=True, nullable=False, sa_column=Column(Integer, ForeignKey("shoppinglist.id", ondelete="CASCADE")))
    shopping_list: "ShoppingList" = Relationship(back_populates="products")
    product_id: int = Field(primary_key=True, foreign_key="product.id", nullable=False)
    product: "Product" = Relationship(back_populates="shopping_lists")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)

class ProductShoppingListRead(ProductShoppingListBase):
    product: Optional["Product"] = None
    created_at: datetime
    updated_at: datetime

class ProductShoppingListCreate(ProductShoppingListBase):
    product_id: int

class ProductShoppingListUpdate(ProductShoppingListBase):
    product_id: int | None = None

# ShoppingList
class ShoppingListBase(SQLModel):
    name: str = Field(nullable=False)

class ShoppingList(ShoppingListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["ProductShoppingList"] = Relationship(back_populates="shopping_list")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)

class ShoppingListRead(ShoppingListBase):
    id: int
    products: List["ProductShoppingListRead"] = []
    created_at: datetime
    updated_at: datetime

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingListUpdate(ShoppingListBase):
    name: str | None = None

# Product
class ProductBase(SQLModel):
    name: str = Field(max_length=100,nullable=False)

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shopping_lists: List["ProductShoppingList"] = Relationship(back_populates="product")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)

class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: str | None = None

# Needed for link to work
ProductShoppingListRead.update_forward_refs()