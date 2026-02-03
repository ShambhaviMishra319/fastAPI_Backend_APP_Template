from src.repository.table import Base
import datetime
import SQLAlchemy

#Mapped tells this is an table attribute of following type ->>use for typing of column
#mapped_column creates actual column
from SQLAlchemy.orm import Mapped,mapped_column

from SQLAlchemy.sql import functions

class Account(Base):
    __tablename__="account"

    id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(SQLAlchemy.String(length=64),nullable=False,unique=True)
    email:Mapped[str]=mapped_column(SQLAlchemy.String(length=1024),nullable=True)
    #CONVENTION (_) to convey to devs that this should not be played with its crucial
    _hashed_password:Mapped[str]=mapped_column(SQLAlchemy.String(length=1024),nullable=True)
    _hash_salt:Mapped[str]=mapped_column(SQLAlchemy.String(length=1024),nullable=True)
    is_verified:Mapped[bool]=mapped_column(SQLAlchemy.Boolean,nullable=False,default=False)
    is_active:Mapped[bool]=mapped_column(SQLAlchemy.Boolean,nullable=False,default=False)
    is_logged_in:Mapped[bool]=mapped_column(SQLAlchemy.Boolean,nullable=False,default=False)

    #tells the database to auto fill at the time of creation =>> SQLAlchemy.datetime(timezone=True),server_default=functions.now()
    created_at:Mapped[datetime.datetime]=mapped_column(SQLAlchemy.Datetime(timezone=True),nullable=False,server_default=functions.now())

    #
    updated_at:Mapped[datetime.datetime]=mapped_column(SQLAlchemy.datetime(timezone=True),nullable=True,server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True))



#Don’t wait. Pull DB-generated values immediately.
    __mapper_args__={"eager_defaults":True}

#without property we have to call like user.hashed_password()
#but we want to write it like a variable and not like function
#with property looks like a variable bvut behaves like a function
    @property
    def hashed_password(self)->str:
        return self._hashed_password
    
    @property
    def set_hashed_password(self,hashed_password:str):
        self._hashed_password=hashed_password

    @property
    def hash_salt(self)->str:
        return self._hash_salt
    
    @property
    def set_hash_salt(self,hash_salt:str):
         self._hash_salt=hash_salt


#Getter and setter exist so data can be changed only in ways the system allows, not in ways developers feel like.