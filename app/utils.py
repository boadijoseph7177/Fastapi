
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(original_passwd):
    return pwd_context.hash(original_passwd)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)