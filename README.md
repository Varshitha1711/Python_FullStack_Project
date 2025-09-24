# Hotel Reservation System

A full-stack hotel reservation system built with Python, Supabase, and a modern frontend.  

This project allows users to manage **rooms**, **customers**, and **bookings**, with automatic **room status updates** based on booking dates. It is designed to be scalable, maintainable, and deployable.

### **Room Management**
- Browse all available rooms with details such as **type, price, and description**.  
- Search for rooms by **date availability**.  
- Instantly see which rooms are **booked**, **available**, or under **maintenance**.

### **Customer Management**
- Create a **customer profile** with your personal information.  
- Update your contact info anytime.  
- View all your **past and current bookings** in one place.

### **Booking Management**
- **Book a room** for a specific date range quickly and easily.  
- Receive **automatic confirmation** if the room is available.  
- **Cancel or modify bookings** before the start date.  
- Get notified if a room becomes unavailable or is booked by someone else.

### **Automatic Room Status Updates**
- Rooms automatically switch between **available** and **booked** based on booking dates.  
- Avoid booking conflicts—system **prevents overbooking automatically**.  
- Always know when a room will become available.


hotel-reservation-system/
├── API
│ └── main.py   
├── frontend
│ ├── app.py
│ └── 
├── src          #core application logic
│ └── db.py
| └── logic.py   #business logic and tasks
├── 
|
├── requirements.txt
├── .env
└── README.md


## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Supabase account 

### Backend Setup
## Clone the repository:

git clone <repository-url>
cd hotel-reservation-system

## Install dependencies

pip install -r requirements.txt

## Set up database tables in Supabase (rooms, customers, bookings).

1.Create a Supabase project

2.Create rooms,bookings,customers tables


rooms table:

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,         -- e.g., Single, Double, Suite
    price NUMERIC(10,2) NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'available'  -- e.g., available, maintenance
);

Bookings table: stores reservations, linked to rooms and customers

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,
    customer_id INT REFERENCES customers(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_date_range CHECK (end_date >= start_date)
);

Customers table:

Create table Customers (cust_id int primary key,
  name varchar(50),
  email varchar(100) unique,
  phone varchar(13) not null,
  city varchar(50)
  );


3.Get your credentials

## Configure your environment variables

1.Create .env file in project root

2.Add your Supabase credentials to .env :

SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supasebase-key"


### Run the application

# Streamlit frontend
streamlit run frontend/app.py

# FastAPI backend

cd API
python main.py

The API will be available at:

## Technical details

# Technologies used :

