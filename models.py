from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Meter(SQLModel, table=True):
    id : Optional [int ] = Field(default=None, primary_key = True)
    meter_no : int = Field(index= True, unique=True)
    customer_name : str = Field()
    email : str = Field()
    address : str = Field()
    
    
class Token(SQLModel, table=True):
    id : Optional[int]= Field(default=None, primary_key = True)    
    token : str = Field(index=True)
    meter_no : int = Field(index= True, foreign_key="meter.meter_no")
    price : float = Field()
    unit : float = Field()
    used : bool = Field(default=False)
    created_at : datetime = Field(default_factory= datetime.utcnow)
    used_at : Optional[datetime] = Field(default=None)
    