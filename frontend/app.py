# frontend/app.py

import streamlit as st
import requests
from datetime import date

BASE_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(page_title="Hotel Reservation System", layout="wide", page_icon="🏨")

st.title("🏨 Hotel Reservation System")
st.markdown("Manage Customers, Rooms, and Bookings effortlessly")

# --- Tabs ---
tabs = st.tabs(["Customers", "Rooms", "Bookings"])

# Utility
def request_with_feedback(method, url, **kwargs):
    with st.spinner("Working..."):
        try:
            resp = requests.request(method, url, timeout=15, **kwargs)
            return resp
        except Exception as ex:
            st.error(f"Request failed: {ex}")
            return None


# --------------------- CUSTOMERS ---------------------
with tabs[0]:
    st.header("Customer Management")

    with st.expander("Add New Customer", expanded=False):
        with st.form("cust_add_form", clear_on_submit=True):
            name = st.text_input("Name", key="cust_name")
            email = st.text_input("Email", key="cust_email")
            phone = st.text_input("Phone", key="cust_phone")
            submitted = st.form_submit_button("Add Customer")
            if submitted:
                if not name or not email or not phone:
                    st.warning("Please fill all fields.")
                else:
                    payload = {"name": name, "email": email, "phone": phone}
                    r = request_with_feedback("POST", f"{BASE_URL}/customers", json=payload)
                    if r and r.status_code == 200:
                        st.success("Customer added successfully!")
                        st.rerun()
                    elif r is not None:
                        st.error(f"Failed to add customer: {r.text}")

    st.subheader("All Customers")
    r = request_with_feedback("GET", f"{BASE_URL}/customers")
    if r.status_code == 200:
        data = r.json()
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.info("No customers found.")
    else:
        st.error("Error fetching customers")

    with st.expander("Update/Delete Customer", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Update Customer**")
            with st.form("cust_update_form"):
                up_id = st.number_input("Customer ID", min_value=1, step=1, key="cust_up_id")
                new_email = st.text_input("New Email", key="cust_up_email")
                new_phone = st.text_input("New Phone", key="cust_up_phone")
                submit_up = st.form_submit_button("Update")
                if submit_up:
                    if not new_email and not new_phone:
                        st.info("Provide email and/or phone to update.")
                    else:
                        payload = {"email": new_email or None, "phone": new_phone or None}
                        r = request_with_feedback("PUT", f"{BASE_URL}/customers/{int(up_id)}", json=payload)
                        if r and r.status_code == 200:
                            st.success("Customer updated.")
                            st.rerun()
                        elif r is not None:
                            st.error(f"Update failed: {r.text}")
        with col2:
            st.markdown("**Delete Customer**")
            with st.form("cust_del_form"):
                del_id = st.number_input("Customer ID to delete", min_value=1, step=1, key="cust_del_id")
                submit_del = st.form_submit_button("Delete")
                if submit_del:
                    r = request_with_feedback("DELETE", f"{BASE_URL}/customers/{int(del_id)}")
                    if r and r.status_code == 200:
                        st.success("Customer deleted.")
                        st.rerun()
                    elif r is not None:
                        st.error(f"Delete failed: {r.text}")

# --------------------- ROOMS ---------------------
with tabs[1]:
    st.header("Room Management")

    with st.expander("Add New Room", expanded=False):
        with st.form("room_add_form", clear_on_submit=True):
            room_type = st.text_input("Room Type", key="room_type")
            price = st.number_input("Price per night", min_value=0.0, step=1.0, key="room_price")
            description = st.text_area("Description", key="room_desc")
            status = st.selectbox("Status", ["available", "maintenance"], key="room_status")
            submit_room = st.form_submit_button("Add Room")
            if submit_room:
                if not room_type or description is None:
                    st.warning("Please provide room type and description.")
                else:
                    payload = {"type": room_type, "price": price, "description": description, "status": status}
                    r = request_with_feedback("POST", f"{BASE_URL}/rooms", json=payload)
                    if r and r.status_code == 200:
                        st.success("Room added successfully!")
                        st.rerun()
                    elif r is not None:
                        st.error(f"Failed to add room: {r.text}")

    st.subheader("All Rooms")
    r = request_with_feedback("GET", f"{BASE_URL}/rooms")
    if r.status_code == 200:
        rooms = r.json()
        if rooms:
            st.dataframe(rooms, use_container_width=True)
        else:
            st.info("No rooms found.")
    else:
        st.error("Error fetching rooms")

    with st.expander("Update/Delete Room", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Update Room**")
            with st.form("room_update_form"):
                room_id = st.number_input("Room ID", min_value=1, step=1, key="room_up_id")
                new_status = st.selectbox("New Status", ["", "available", "maintenance", "booked"], key="room_up_status")
                new_price = st.number_input("New Price (optional)", min_value=0.0, step=1.0, key="room_up_price")
                submit_room_up = st.form_submit_button("Update")
                if submit_room_up:
                    last_resp = None
                    if new_status:
                        last_resp = request_with_feedback("PUT", f"{BASE_URL}/rooms/{int(room_id)}", json={"status": new_status})
                    if new_price and new_price > 0:
                        last_resp = request_with_feedback("PUT", f"{BASE_URL}/rooms/{int(room_id)}", json={"price": float(new_price)})
                    if last_resp and last_resp.status_code == 200:
                        st.success("Room updated.")
                        st.rerun()
                    elif last_resp is not None:
                        st.error(f"Update failed: {last_resp.text}")
        with col2:
            st.markdown("**Delete Room**")
            with st.form("room_del_form"):
                del_room_id = st.number_input("Room ID to delete", min_value=1, step=1, key="room_del_id")
                submit_room_del = st.form_submit_button("Delete")
                if submit_room_del:
                    r = request_with_feedback("DELETE", f"{BASE_URL}/rooms/{int(del_room_id)}")
                    if r and r.status_code == 200:
                        st.success("Room deleted.")
                        st.rerun()
                    elif r is not None:
                        st.error(f"Delete failed: {r.text}")

# --------------------- BOOKINGS ---------------------
with tabs[2]:
    st.header("Booking Management")

    with st.expander("Add Booking", expanded=False):
        customers_r = request_with_feedback("GET", f"{BASE_URL}/customers")
        rooms_r = request_with_feedback("GET", f"{BASE_URL}/rooms")
        customers_r = customers_r.json() if customers_r and customers_r.status_code == 200 else []
        rooms_r = rooms_r.json() if rooms_r and rooms_r.status_code == 200 else []

        cust_dict = {f"{c['name']} ({c['cust_id']})": c['cust_id'] for c in customers_r} if customers_r else {}
        room_dict = {f"{r['type']} - {r['id']}": r['id'] for r in rooms_r if r.get('status') == "available"} if rooms_r else {}

        cust_options = list(cust_dict.keys())
        room_options = list(room_dict.keys())

        if not cust_options:
            st.info("No customers available. Add a customer first.")
        if not room_options:
            st.info("No available rooms. Add a room or free an existing one.")

        customer_sel = st.selectbox("Select Customer", cust_options or [""], index=0 if cust_options else None, key="book_cust")
        room_sel = st.selectbox("Select Room", room_options or [""], index=0 if room_options else None, key="book_room")
        start = st.date_input("Start Date", min_value=date.today(), key="start_date")
        end = st.date_input("End Date", min_value=start, key="end_date")

        can_submit = bool(customer_sel in cust_dict and room_sel in room_dict)
        submit_disabled = not can_submit
        add_btn = st.button("Add Booking", key="add_booking", disabled=submit_disabled)
        if add_btn and can_submit:
            payload = {
                "customer_id": cust_dict.get(customer_sel),
                "room_id": room_dict.get(room_sel),
                "start_date": str(start),
                "end_date": str(end)
            }
            r = request_with_feedback("POST", f"{BASE_URL}/bookings", params=payload)
            if r and r.status_code == 200:
                st.success("Booking added successfully!")
                st.rerun()
            elif r is not None:
                st.error(f"Failed to add booking: {r.text}")

    st.subheader("All Bookings")
    r = request_with_feedback("GET", f"{BASE_URL}/bookings")
    if r.status_code == 200:
        bookings = r.json()
        if bookings:
            st.dataframe(bookings, use_container_width=True)
        else:
            st.info("No bookings found.")
    else:
        st.error("Error fetching bookings")

    with st.expander("Cancel Booking", expanded=False):
        with st.form("booking_cancel_form"):
            booking_id = st.number_input("Booking ID", min_value=1, step=1, key="book_cancel_id")
            cancel_btn = st.form_submit_button("Cancel Booking")
            if cancel_btn:
                r = request_with_feedback("DELETE", f"{BASE_URL}/bookings/{int(booking_id)}")
                if r and r.status_code == 200:
                    st.success("Booking cancelled.")
                    st.rerun()
                elif r is not None:
                    st.error(f"Cancel failed: {r.text}")
