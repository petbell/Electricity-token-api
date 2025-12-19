from sqlmodel import SQLModel

class MeterCreate(SQLModel):
    meter_no : int 
    customer_name : str 
    address : str 

class TokenCreate(SQLModel):
    # meter_no : int  no need for this because it would come from a dependency
    price : float 
    #unit : float 

class TokenResponse(SQLModel):
    id : int
    token : str
    meter_no : int  
    price : float 
    unit : float 
