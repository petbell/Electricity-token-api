from typing import Annotated
from sqlmodel import SQLModel, Field
from datetime import datetime


class Meter(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key = True)
    meter_no : int = Field(index= True, unique=True)
    customer_name : str = Field()
    address : str = Field()
    
    
class Token(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key = True)    
    token : int = Field(index=True)
    meter_no : int = Field(index= True, foreign_key="meter")
    price : float = Field()
    unit : float = Field()
    used : bool = Field(default=False)
    created_at : datetime = Field(default_factory= datetime.utcnow)
    used_at : datetime = Field()
    