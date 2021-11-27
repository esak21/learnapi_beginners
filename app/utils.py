from passlib.context import CryptContext
from passlib.utils.decor import deprecated_function

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password:str):
    return password_context.hash(password)


def verifyPassword(plainPassword, hashPassword):
    return password_context.verify(plainPassword, hashPassword)