from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException, BackgroundTasks
from sqlmodel import  select
import datetime
from database import create_db_and_table, SessionDep
from schemas import MeterCreate, TokenCreate, TokenResponse
from models import Meter, Token
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import dotenv

dotenv.load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@agrovet.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")



app = FastAPI(title= "Electricity Token")

# ========== Email Sending Function ==========
def send_email(to_email: str, subject: str, body: str):
    """Send an email to the specified recipient in background."""
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {str(e)}")
        
def send_token_email(to_email: str, name:str, token: str, background_task : BackgroundTasks):
    subject = "Your Electricity Token"
    body = f"""
    <html>
    <body>

        <h2>Your Electricity Token</h2>
        <h3> Hi {name},</h3>
        <p>Here is your electricity token: <strong>{token}</strong></p>
        <p>Thank you for using our service!</p>
    </body>
    </html>
    """
    background_task.add_task(send_email, to_email, subject, body)
    print ("Email task added to background tasks.")

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
    statement = select (Meter).where(Meter.meter_no == meter_id)
    meter = session.exec(statement).first()
    
    return meter

@app.post("/token/", response_model=TokenResponse)
def create_token(token_data : TokenCreate, session : SessionDep,
                 meter : Annotated[Meter, Depends(get_meter)],
                                   background_task : BackgroundTasks):
    print("start function")
    token_val = str(random.randint(10**19, 10**20 - 1))
    
    meter_number = meter.meter_no
    email = meter.email
    name = meter.customer_name
    kwh = 50.823
    price = token_data.price
    unit = price / kwh
    record = Token(
        token = token_val,
        meter_no = meter_number,
        price = token_data.price,
        unit = unit   
    )
    print (price)
    print (meter_number)
    print (token_val.split(" ",4))
    print (unit)
    session.add(record)
    session.commit()
    session.refresh(record)
    
    print( f" Utility Toens is: {token_val.split(" ",4)}")
    print (f"You get {unit} units")
    
    
    send_token_email(email, name, token_val, background_task)
    
    return record
    # token = Token(**token.model_dump())
    