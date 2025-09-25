#db.py

import os
from supabase import create_client
from dotenv import load_dotenv

#loading environmental variables
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
sb=create_client(url,key)

#create customer
def create_customers(name,email,phone):
    return sb.table("customers").insert({"name":name,"email":email,"phone":phone}).execute()

#register a room
def register_room(type,price ,description,status):
    return sb.table("rooms").insert({"type":type,"price":price,"description":description,"status":status}).execute()

#make a booking
def make_booking(room_id,customer_id ,start_date,end_date):

    # 1. Check room status
    room = sb.table("rooms").select("status").eq("id", room_id).execute()
    if not room.data:
        return {"error": "Room not found."}

    if room.data[0]["status"] != "available":
        return {"error": "Room is not available."}

    # 2. Create the booking
    booking = sb.table("bookings").insert(
        {
            "customer_id": customer_id,
            "room_id": room_id,
            "start_date": start_date,
            "end_date": end_date,
        }
    ).execute()

    # 3. Update room status → "booked"
    sb.table("rooms").update({"status": "booked"}).eq("id", room_id).execute()

    return booking.data