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
    username: str = Field(unique=True)
    email: str | None = Field(default=None, unique=True)
    first_name: str | None = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default = None, primary_key=True)
    password: str

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    password: str
    repeat_password: str

class UserUpdate(UserBase):
    pass

# Product-ShoppingList association table 
class ProductShoppingListBase(SQLModel):
    price: int | None
    amount_to_buy: int | None
    amount_bought: int | None

class ProductShoppingList(ProductShoppingListBase, table=True):
    shopping_list_id: Optional[int] = Field(primary_key=True, default=None, sa_column=Column(Integer, ForeignKey("shoppinglist.id", ondelete="CASCADE"))) #Field(default=None, foreign_key="shoppinglist.id", primary_key=True)
    shopping_list: "ShoppingList" = Relationship(back_populates="products")
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    product: "Product" = Relationship(back_populates="shopping_lists")

class ProductShoppingListRead(ProductShoppingListBase):
    product: Optional["Product"] = None

class ProductShoppingListCreate(ProductShoppingListBase):
    product_id: int

# ShoppingList
class ShoppingListBase(SQLModel):
    name: str

class ShoppingList(ShoppingListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["ProductShoppingList"] = Relationship(back_populates="shopping_list")
    created_at: Optional[datetime] = Field(default=datetime.now())

class ShoppingListRead(ShoppingListBase):
    id: int
    products: List["ProductShoppingListRead"] = []
    created_at: datetime

class ShoppingListCreate(ShoppingListBase):
    name: str

class ShoppingListUpdate(ShoppingListBase):
    name: str

# Product
class ProductBase(SQLModel):
    name: str

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shopping_lists: List["ProductShoppingList"] = Relationship(back_populates="product")

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    name: str

class ProductUpdate(ProductBase):
    name: str

# Needed for link to work
ProductShoppingListRead.update_forward_refs()