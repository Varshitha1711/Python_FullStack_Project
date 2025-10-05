
from src.db import DatabaseManager

#Acts as bridge between frontend(streamlit/FastAPI ) and Backend
class CustomerManager:

    def __init__(self):
        """create a database manager instance (will handle the database operations)"""
        self.db=DatabaseManager()

    def add_customer(self,name,email,phone):
        res=self.db.create_customers(name,email,phone)
        # Supabase responses expose .data and optionally .error
        if getattr(res, "data", None) and not getattr(res, "error", None):
            return {"Success": True, "Message": "Customer added successfully"}
        return {"Success": False, "Message": f"Error: {getattr(res, 'error', None)}"}
        
    def get_all_cust(self):
        return self.db.get_customers()
    
    def delete_cust(self,id):
        res=self.db.delete_customer(id)
        if getattr(res, "data", None) is not None and not getattr(res, "error", None):
            return {"Success": True, "Message": "Customer deleted successfully"}
        return {"Success": False, "Message": f"Error: {getattr(res, 'error', None)}"}
        
    def update_email(self,id,email):
        res=self.db.update_customer(cust_id=id,email=email)
        if getattr(res, "data", None) and not getattr(res, "error", None):
            return {"Success": True, "Message": "Email updated successfully"}
        return {"Success": False, "Message": f"Error: {getattr(res, 'error', None)}"}
    
    def update_phone(self,id,phone):
        res=self.db.update_customer(cust_id=id,phone=phone)
        if getattr(res, "data", None) and not getattr(res, "error", None):
            return {"Success": True, "Message": "Phone number updated successfully"}
        return {"Success": False, "Message": f"Error: {getattr(res, 'error', None)}"}

class RoomManager:
    def __init__(self):
        self.db=DatabaseManager()

    def add_room(self,type,price,description,status):
        res=self.db.register_room(type,price,description,status)
        if getattr(res, "data", None) and not getattr(res, "error", None):
            return {"Success": True, "Message": "Room successfully added"}
        return {"Success": False, "Error": f"{getattr(res, 'error', None)}"}
    
    def get_all_rooms(self):
        return self.db.get_rooms()
    
    def update_status(self,room_id,status):
        res=self.db.update_room(room_id,status=status)
        if getattr(res, "data", None) and not getattr(res, "error", None):
            return {"Success": True, "Message": "Room status updated successfully"}
        return {"Success": False, "Error": f"{getattr(res, 'error', None)}"}

    def update_price(self,room_id,price):
        res=self.db.update_room(room_id,price=price)
        if getattr(res, "data", None) and not getattr(res, "error", None):
            return {"Success": True, "Message": "Room price updated successfully"}
        return {"Success": False, "Error": f"{getattr(res, 'error', None)}"}  
    
    def delete_room(self,id):
        res=self.db.delete_room(id)
        if getattr(res, "data", None) is not None and not getattr(res, "error", None):
            return {"Success": True, "Message": "Room deleted successfully"}
        return {"Success": False, "Message": f"Error: {getattr(res, 'error', None)}"}
        
class BookingManager:
    def __init__(self):
        self.db=DatabaseManager()
    
    # Match API signature: customer_id, room_id, start_date, end_date
    def add_booking(self,customer_id, room_id, start_date, end_date):
        res=self.db.make_booking(room_id, customer_id, start_date, end_date)
        if isinstance(res, dict) and res.get("error"):
            return {"Success": False, "Message": f"Error: {res.get('error')}"}
        if isinstance(res, list) or getattr(res, "data", None):
            return {"Success": True, "Message": "Booking successful"}
        return {"Success": False, "Message": "Error: Unknown booking failure"}
        
    def display_book(self):
        return self.db.get_bookings()
    
    def cancel_booking(self, booking_id):
        res = self.db.cancel_booking(booking_id)
        if isinstance(res, dict) and res.get("success"):
            return {"Success": True, "Message": res.get("success")}
        return {"Success": False, "Message": f"Error: {res.get('error')}"}
    
    
