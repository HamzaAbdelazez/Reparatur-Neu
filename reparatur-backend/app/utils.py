from passlib.context import CryptContext

# إعداد التشفير
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# دالة لتشفير كلمة المرور
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# دالة لمقارنة كلمة المرور المُدخلة مع المشفّرة
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
