
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase

#Because all other tables inherit from Base, all of them get registered inside metadata.
class Base(DeclarativeBase):
    metadata:sqlalchemy.metadata=sqlalchemy.metadata