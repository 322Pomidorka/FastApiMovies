import os
from jose import jwt
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv

from users.dao import UsersDAO

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_auth_data():
    return {"secret_key": os.getenv("SECRET_KEY"), "algorithm": os.getenv("ALGORITHM")}

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(login_name: str, password: str):
    user = await UsersDAO.find_one_or_none(login_name=login_name)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user