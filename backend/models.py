from pydantic import condecimal
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# AccessToken
class AccessToken(SQLModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshToken(SQLModel):
    refresh_token: str


# User-ShoppingList association table
class UserShoppingListBase(SQLModel):
    owner: bool = Field(default=False, nullable=False)


class UserShoppingList(UserShoppingListBase, table=True):
    shopping_list_id: int = Field(primary_key=True, nullable=False, foreign_key="shoppinglist.id")
    shopping_list: "ShoppingList" = Relationship(back_populates="users")
    user_id: int = Field(primary_key=True, nullable=False, foreign_key="user.id")
    user: "User" = Relationship()


class UserShoppingListRead(UserShoppingListBase):
    owner: bool
    user_id: int

# User
class UserBase(SQLModel):
    username: str = Field(unique=True, min_length=4, max_length=16, nullable=False)
    email: str = Field(unique=True, max_length=320, nullable=False)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    password: str = Field(max_length=255, nullable=False)
    shopping_list: "UserShoppingList" = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "delete"})


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
    repeat_password: str


class UserUpdate(UserBase):
    pass

# Product-ShoppingList association table
class ProductShoppingListBase(SQLModel):
    price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(default=0, nullable=True)
    amount_to_buy: Decimal | None = Field(default=1, nullable=True)
    amount_bought: Decimal | None = Field(default=0, nullable=True)
    completed: bool | None = Field(default=False)


class ProductShoppingList(ProductShoppingListBase, table=True):
    shopping_list_id: int = Field(primary_key=True, nullable=False, foreign_key="shoppinglist.id")
    shopping_list: "ShoppingList" = Relationship(back_populates="products")
    product_id: int = Field(primary_key=True, foreign_key="product.id", nullable=False)
    product: "Product" = Relationship(back_populates="shopping_lists")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)


class ProductShoppingListRead(ProductShoppingListBase):
    product: Optional["ProductRead"] = None
    created_at: datetime
    updated_at: datetime


class ProductShoppingListCreate(ProductShoppingListBase):
    product_id: int
    shopping_list_id: int | None


class ProductShoppingListUpdate(ProductShoppingListBase):
    product_id: int | None = None

# ShoppingList
class ShoppingListBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)


class ShoppingList(ShoppingListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["ProductShoppingList"] = Relationship(back_populates="shopping_list", sa_relationship_kwargs={"cascade": "delete"})
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    users: List["UserShoppingList"] = Relationship(back_populates="shopping_list", sa_relationship_kwargs={"cascade": "delete"})


class ShoppingListRead(ShoppingListBase):
    id: int
    products: List["ProductShoppingListRead"] = []
    created_at: datetime
    updated_at: datetime
    users: List["UserShoppingListRead"] = []


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingListUpdate(ShoppingListBase):
    name: str | None = None

# Unit
class UnitBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)
    precision: Optional[int] = Field(default=0)


class Unit(UnitBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product: "Product" = Relationship(back_populates="unit")


class UnitRead(UnitBase):
    pass


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    name: str | None = None
    precision: int | None = None


# Product
class ProductBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shopping_lists: List["ProductShoppingList"] = Relationship(back_populates="product")
    created_at: datetime = Field(default=datetime.now(), nullable=False)
    updated_at: datetime = Field(default=datetime.now(), nullable=False)
    unit_id: int = Field(foreign_key="unit.id")
    unit: "Unit" = Relationship()


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    unit: "UnitRead"


class ProductCreate(ProductBase):
    unit_id: int


class ProductUpdate(ProductBase):
    name: str | None = None
    unit_id: int | None = None


# Needed for link to work
ProductShoppingListRead.update_forward_refs()
