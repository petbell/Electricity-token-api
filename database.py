from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

connect_args = {"check_same_thread": False}

engine = create_engine("sqlite:///electricity_db.db", connect_args=connect_args, echo=False)

# creatw db and tables on start
def create_db_and_table():
    SQLModel.metadata.create_all(engine)

# get db session and automatically closse the connection
def get_session():
    with Session(engine) as session:
        yield session
        
# Session dependency    
SessionDep = Annotated[Session, Depends(get_session)]