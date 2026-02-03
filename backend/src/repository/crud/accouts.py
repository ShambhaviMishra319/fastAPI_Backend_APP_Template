from repository.crud.base import BaseCRUDRepository
from src.models.schemas.account import AccountInCreate,AccountInLogin,AccountInResponse,AccountInUpdate,AccountWithToken
from src.models.db.account import Account
from src.securities.hashing.password import pwd_generator
import sqlalchemy
from  sqlalchemy import select



class AcountCRUDRepository(BaseCRUDRepository):
    async def create_account(self,create_account:AccountInCreate)->Account:

        new_account=Account(username=create_account.username,email=create_account.email,is_logged_in=True)

        new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_account.set_hashed_password(
             hashed_password=pwd_generator.generate_hashed_password(
                  hash_salt=new_account.hash_salt,new_password=create_account.password
             )
        )

        self.async_session.add(instance=new_account)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_account)

        return new_account
    
    async def read_account(self,id:int)->Account:
        smt=SQLAlchemy.select(Account).where(Account.id==id)
        query=await self.async_session.execute(smt)

        if not query:
            raise Exception("Acoount with username `{username}` does not exist !!")
        
        return query.scalar()
        
    async def read_account_by_username(self,username:str)->Account:
        smt=SQLAlchemy.select(Account).where(Account.username==username)
        query=await self.async_session.execute(smt)

        if not query:
            raise Exception("Acoount with username `{username}` does not exist !!")
        
        return query.scalar()

        
    async def read_account_by_email(self,email:str)->Account:
        smt=SQLAlchemy.select(Account).where(Account.email==email)
        query=await self.async_session.execute(smt)

        if not query:
            raise Exception("Acoount with email `{email}` does not exist !!")
        
        return query.scalar()

        
