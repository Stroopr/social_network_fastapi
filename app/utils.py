from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pwd_hasher(password: str):
    return pwd_context.hash(password)

def pwd_verifier(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)