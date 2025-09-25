from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys,os

#Import CustomerManager from src/logic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic import CustomerManager,BookingManager,RoomManager  

# ------------App SetUp----------

app=FastAPI(title="Hotel reservation system API",version='1.0')


# --------------Allow frontend to call API -----------------

app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_header=["*"],
)


#creating a customer manager instance
cust_manager=CustomerManager()
room_manager=RoomManager()
book_manager=BookingManager()

# -----------Data Models------------

class cust_create(BaseModel):
    name:str
    email:str
    phone:str

class cust_update(BaseModel):
    email:str =None
    phone:str =None

class RoomCreate(BaseModel):
    type:str
    price:float
    descrption:str
    status:str="available"

class RoomUpdate(BaseModel):
    status:str =None
    price:float =None

class Bookingcreate(BaseModel):
    customer_id:int
    room_id:int
    start_date:str
    end_date:str




@app.get("/")

def home():
    return{"Message":"Hotel reservation system API is running"}

# -------------Customers-----------------

@app.get("/customers")
def list_customers():
    return cust_manager.get_all_cust().data

@app.post("/customers")
def create_cust(customer:cust_create):
    return cust_manager.add_customer(customer.name,customer.email,customer.phone)

@app.put("/customers/{cust_id}")
def update_customer(cust_id: int, customer: cust_update):
    res = {}
    if customer.email:
        res = cust_manager.update_email(cust_id, customer.email)
    if customer.phone:
        res = cust_manager.update_phone(cust_id, customer.phone)
    return res

@app.delete("/customer/{cust_id}")
def delete_customer(cust_id:int):
    return cust_manager.delete_cust(cust_id)

# -----------------Rooms-----------------------

@app.get("/rooms")
def list_rooms():
    return room_manager.get_all_rooms().data

@app.post("/rooms")
def create_room(room:RoomCreate):
    return room_manager.add_room(room.type,room.price,room.descrption,room.status)

@app.put("/rooms/{room_id}")
def update_room(room_id:int,room:RoomUpdate):
    if room.status:
        res=room_manager.update_status(room_id,room.status)
    if room.price:
        res=room_manager.update_price(room_id,room.price)
    return res

@app.delete("/rooms/{room_id}")
def delete_room(room_id:int):
    return room_manager.delete_room(room_id)

# ------------------Bookings----------------------

@app.get("/bookings")
def list_bookings():
    return book_manager.display_book().data

@app.post("/bookings")
def add_book(customer_id: int, room_id: int, start_date: str, end_date: str):
    return book_manager.add_booking(customer_id, room_id, start_date, end_date)

@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    res = book_manager.cancel_booking(booking_id)
    if not res["Success"]:
        raise HTTPException(status_code=400, detail=res["Message"])
    return res


if __name__=="__main__":
    import uvicorn