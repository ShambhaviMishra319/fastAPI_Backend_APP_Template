import pydantic
import datetime
from src.models.schemas.jwt import JWToken,JWTAccount
from src.config.manager import settings
from src.models.db.account import Account
from jose import jwt,JWTError

class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
            self,
            *,
            jwt_data:dict[str,str],
            expires:datetime.timedelta |None=None
    ):
        
        if expires:
            expires_in=datetime.datetime.utcnow()+expires
        else:
            expires_in=datetime.datetime.utcnow()+datetime.timedelta(minutes=5)

        to_encode=jwt_data.copy()
        to_encode.update(JWToken(exp=expires_in,sub=settings.JWT_SUBJECT).dict())
        encoded=jwt.encode(to_encode,key=settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

        return encoded

    def generate_access_token(self,account:Account)->str:
        if not account:
            raise Exception(f"entity not found")

        return self._generate_jwt_token(
            jwt_data=JWTAccount(username=account.username,email=account.email).dict(),
            expires=datetime.timedelta(minutes=5))

    def retrieve_details_from_token(self,token:str,secret_key:str)->list[str]:
        try:
            #decode → dict
            payload=jwt.decode(token=token,key=secret_key,algorithms=[settings.JWT_ALGORITHM])
            jwt_account=JWTAccount(username=payload['username'],email=payload['email'])
        except JWTError:
            raise ValueError("invalid payload")
        
        return [jwt_account.username,jwt_account.email]


##DEPENDENCY INJECTION (not yet)
##factory function
def get_jwt_generator()->JWTGenerator:
    return JWTGenerator()

##module level singleton
jwt_generator:JWTGenerator= get_jwt_generator()