from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashing_password(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
