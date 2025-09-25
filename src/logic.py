
from src.db import DatabaseManager

#Acts as bridge between frontend(streamlit/FastAPI ) and Backend
class CustomerManager:

    def __init__(self):
        """create a database manager instance (will handle the database operations)"""
        self.db=DatabaseManager()

    def add_customer(self,name,email,phone):
        res=self.db.create_customers(name,email,phone)
        if res.get("Success"):
            return {"Success":True,"Message":"Customer added successfully"}
        else:
            return {"Success":False,"Message":f"Error:{res.get('error')}"}
        
    def get_all_cust(self):
        return self.db.get_customers()
    
    def delete_cust(self,id):
        res=self.db.delete_customers(id)
        if res.get("Success"):
            return {"Success":True,"Message":"Customer deleted successfully"}
        else:
            return {"Success":False,"Message":f"Error:{res.get("error")}"}
        
    def update_email(self,id,email):
        res=self.db.update_customer(cust_id=id,email=email)
        if res.get("Success"):
            return {"Success":True,"Message":"Email updated successfully"}
        else:
            return {"Success":False,"Message":f"Error {res.get('error')}"}
    
    def update_phone(self,id,phone):
        res=self.db.update_customer(cust_id=id,phone=phone)
        if res.get("Success"):
            return {"Success":True,"Message":"Phone number updated successfully"}
        else:
            return {"Success":False,"Message":f"Error {res.get('error')}"}

class RoomManager:
    def __init__(self):
        self.db=DatabaseManager()

    def add_room(self,type,price,description,status):
        res=self.db.register_room(type,price,description,status)
        if res.get("Success"):
            return {"Success":True,"Message":"Room successfully added"}
        else:
            return{"Success":False,"Error":f"{res.get("error")}"}
    
    def get_all_rooms(self):
        return self.db.get_rooms()
    
    def update_status(self,status):
        res=self.db.update_rooms(status=status)
        if res.get("Success"):
            return {"Success":True,"Message":"Room status updated successfully "}
        else:
            return{"Success":False,"Error":f"{res.get("error")}"}

    def update_price(self,price):
        res=self.db.upadte_rooms(price=price)
        if res.get("Success"):
            return {"Success":True,"Message":"Room status updated successfully "}
        else:
            return{"Success":False,"Error":f"{res.get("error")}"}  
    
    def delete_room(self,id):
        res=self.db.delete_room(id)
        if res.get("Success"):
            return {"Success":True,"Message":"Room deleted successfully"}
        else:
            return {"Success":False,"Message":f"Error:{res.get("error")}"}
        
class BookingManager:
    def __init__(self):
        self.db=DatabaseManager()
    
    def add_booking(self,room_id,cust_id,start,end):
        res=self.db.make_booking(room_id,cust_id,start,end)
        if res.get("Success"):
            return {"Success":True,"Message":"Booking successfully"}
        else:
            return{"Success":False,"Message":f"Error:{res.get("error")}"}
        
    def display_book(self):
        return self.db.get_bookings()
    
    def cancel_booking(self, booking_id):
        res = self.db.cancel_booking(booking_id)
        if res.get("success"):
            return {"Success": True, "Message": res.get("success")}
        return {"Success": False, "Message": f"Error: {res.get('error')}"}
    
    
