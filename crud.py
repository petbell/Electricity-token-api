from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException
from sqlmodel import  select
import datetime
from database import create_db_and_table, SessionDep
from schemas import MeterCreate, TokenCreate
from models import Meter, Token
import random

app = FastAPI(title= "Electricity Token")

@app.on_event("startup")
def on_startup():
    create_db_and_table()


@app.post("/meter/")
def add_meter (meter : MeterCreate, session : SessionDep):
    meter = Meter(**meter.model_dump())
    session.add(meter)
    session.commit()
    session.refresh(meter)
    return meter

@app.get("/meter/{meter_id}", response_model=MeterCreate)
def  get_meter ( meter_id : int, session : SessionDep):
    statement = select (Meter).where(Meter.meter_no == id)
    meter = session.exec(statement).first()
    
    return meter

@app.post("/token/", response_model=TokenCreate)
def create_token(token_data : TokenCreate, session : SessionDep, meter : Annotated[Meter, Depends(get_meter)]):
    token = random.randint(10**19, 10**20 - 1)
    meter_number = meter.meter_no
    kwh = 50.823
    price = token_data.price
    unit = price / kwh
    record = Token(
        token = token,
        meter_no = meter_number,
        price = token_data.price,
        unit = unit   
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    
    print( f" Utility Toens is: {token}")
    print (f"You get {kwh} units")
    
    return record
    # token = Token(**token.model_dump())
    