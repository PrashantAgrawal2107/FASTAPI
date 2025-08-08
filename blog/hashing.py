from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password : str):
        hashed_password = pwd_context.hash(password)
        return hashed_password
    
    def verify(hashed_pwd , plain_pwd):
        return pwd_context.verify(plain_pwd,hashed_pwd)
