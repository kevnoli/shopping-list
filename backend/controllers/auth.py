from fastapi import Depends, HTTPException, Response, status
from redis import Redis
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from datetime import timedelta, datetime
from dotenv import load_dotenv
from os import getenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db import get_session, get_redis_client
from models import User, UserCreate, AccessToken, RefreshToken

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

load_dotenv()
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = getenv("JWT_REFRESH_SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.get(User, user_id)
    if user is None or not verify_token(user.id, "access", token):
        raise credentials_exception
    return user

def add_token_to_redis(user_id: int, token_type: str, token: str, expire: datetime) -> None:
    redis_client = get_redis_client()
    key = f"user:{user_id}:{token_type}"
    redis_client.set(key, token)
    redis_client.expireat(key, expire)

def verify_token(user_id: int, token_type: str, token: str) -> bool:
    redis_client = get_redis_client()
    key = f"user:{user_id}:{token_type}"
    if redis_client.get(key) == token:
        return True
    else:
        return False

def create_jwt_token(subject: int, token_type: str = "access") -> str: #nosec B107
    expire = datetime.utcnow() + timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES" if token_type == "access" else "REFRESH_TOKEN_EXPIRE_MINUTES"))) # nosec B105
    to_encode = { "sub": str(subject), "exp": expire, "iat": datetime.utcnow() }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY if token_type == "access" else JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM) # nosec B105
    add_token_to_redis(subject, token_type, encoded_jwt, expire)
    return encoded_jwt

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate(username: str, password: str, db: Session = Depends(get_session)) -> User:
    statement = select(User).where(username == username)
    user = db.exec(statement).one()
    if not user or not verify_password(password, user.password):
        raise credentials_exception
    return user

async def token(response: Response, form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    user = authenticate(username=form_data.username, password=form_data.password, db=db)
    access_token = create_jwt_token(subject=user.id, token_type="access") # nosec B106
    refresh_token = create_jwt_token(subject=user.id, token_type="refresh") # nosec B106
    return AccessToken(access_token=access_token, token_type="bearer", refresh_token=refresh_token)

async def register(user: UserCreate, db: Session = Depends(get_session)):
    try:
        if user.password == user.repeat_password:
            user.password = get_hash(user.password)
            user_dict = dict(user)
            db_user = User.parse_obj(user_dict)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password confirmation does not match")
    except IntegrityError as exc:
        constraint_name = exc.orig.diag.constraint_name
        if constraint_name == "user_username_key":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Username "{user.username}" is already taken')
        if constraint_name == "user_email_key":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'E-mail "{user.email}" is already being used')

async def refresh(refresh_token : RefreshToken, db: Session = Depends(get_session)):
    payload = jwt.decode(refresh_token.refresh_token, key=JWT_REFRESH_SECRET_KEY, algorithms=ALGORITHM)
    if verify_token(payload.get("sub"), "refresh", refresh_token.refresh_token):
        user_id = payload.get("sub")
        if db.get(User, user_id):
            access_token = create_jwt_token(id)
            add_token_to_redis(user_id, "access", access_token, datetime.utcnow() + timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
            return AccessToken(access_token=access_token, token_type="bearer", refresh_token=refresh_token.refresh_token) # nosec B106
    else:
        raise credentials_exception

async def get_user(user: User = Depends(get_current_user)):
    return user

async def signout(user: User = Depends(get_current_user)):
    get_redis_client().delete(f"user:{user.id}:access")
    get_redis_client().delete(f"user:{user.id}:refresh")
    return None