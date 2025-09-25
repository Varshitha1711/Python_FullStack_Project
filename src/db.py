#db.py

import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()
#loading environmental variables
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
sb=create_client(url,key)



class DatabaseManager:

    # Customers

    def create_customers(self, name, email, phone):
        return sb.table("customers_h").insert({"name": name, "email": email, "phone": phone}).execute()

    def get_customers(self):
        return sb.table("customers_h").select("*").execute()

    def update_customer(self, cust_id: int, name: str = None, email: str = None, phone: str = None):
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        return sb.table("customers_h").update(data).eq("cust_id", cust_id).execute()

    def delete_customer(self, cust_id: int):
        return sb.table("customers_h").delete().eq("cust_id", cust_id).execute()


# Rooms
def register_room(type, price, description, status):
    return sb.table("rooms").insert({"type": type, "price": price, "description": description, "status": status}).execute()

def get_rooms():
    return sb.table("rooms").select("*").execute()


def update_room(room_id: int, room_type: str = None, price: float = None, description: str = None, status: str = None):
    data = {}
    if room_type:
        data["type"] = room_type
    if price is not None:
        data["price"] = price
    if description:
        data["description"] = description
    if status:
        data["status"] = status
    return sb.table("rooms").update(data).eq("id", room_id).execute()


def delete_room(room_id: int):
    return sb.table("rooms").delete().eq("id", room_id).execute()


# Bookings
def make_booking(room_id, customer_id, start_date, end_date):
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


def get_bookings():
    return sb.table("bookings").select("*").execute()


# Set rooms back to 'available' if their bookings have ended
def reset_room_statuses():
    today = str(date.today())
    ended_bookings = sb.table("bookings").select("room_id, end_date").lt("end_date", today).execute()
    room_ids_to_reset = {b["room_id"] for b in ended_bookings.data}
    if room_ids_to_reset:
        sb.table("rooms").update({"status": "available"}).in_("id", list(room_ids_to_reset)).execute()
        print(f"Reset status for rooms: {list(room_ids_to_reset)}")
    else:
        print("No rooms to reset today.")


scheduler = BackgroundScheduler()
# runs every 24 hours
scheduler.add_job(reset_room_statuses, 'interval', hours=24)
scheduler.start()
print("Scheduler started: Room status auto-reset is active.")


def cancel_booking(booking_id: int):
    """Delete a booking and update room status if necessary"""
    booking = sb.table("bookings").select("*").eq("id", booking_id).execute()
    if not booking.data:
        return {"error": "Booking not found."}

    room_id = booking.data[0]["room_id"]
    sb.table("bookings").delete().eq("id", booking_id).execute()

    # Check if room has any other future bookings
    future_bookings = sb.table("bookings").select("*").eq("room_id", room_id).gte("end_date", str(date.today())).execute()
    if not future_bookings.data:
        sb.table("rooms").update({"status": "available"}).eq("id", room_id).execute()

    return {"success": f"Booking {booking_id} cancelled."}
