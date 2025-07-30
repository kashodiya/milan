


import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import the database models
import sys
sys.path.append('backend')
from database import Base, engine
import models

# Create the database tables
Base.metadata.create_all(bind=engine)

# Connect to the database
conn = sqlite3.connect('backend/matrimonial.db')
cursor = conn.cursor()

# Check if tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Function to hash passwords
def hash_password(password):
    # Use bcrypt for password hashing
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

# Create some test users
test_users = [
    {
        "email": "john@example.com",
        "password": "password123",
        "gender": "male",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-15",
        "height": 175.5,
        "religion": "Hindu",
        "marital_status": "never_married",
        "occupation": "Software Engineer",
        "education": "Master's Degree",
        "location_city": "Mumbai",
        "location_state": "Maharashtra",
        "location_country": "India"
    },
    {
        "email": "jane@example.com",
        "password": "password123",
        "gender": "female",
        "first_name": "Jane",
        "last_name": "Smith",
        "date_of_birth": "1992-05-20",
        "height": 165.0,
        "religion": "Hindu",
        "marital_status": "never_married",
        "occupation": "Doctor",
        "education": "Medical Degree",
        "location_city": "Delhi",
        "location_state": "Delhi",
        "location_country": "India"
    },
    {
        "email": "michael@example.com",
        "password": "password123",
        "gender": "male",
        "first_name": "Michael",
        "last_name": "Johnson",
        "date_of_birth": "1988-11-10",
        "height": 180.0,
        "religion": "Christian",
        "marital_status": "never_married",
        "occupation": "Architect",
        "education": "Bachelor's Degree",
        "location_city": "Bangalore",
        "location_state": "Karnataka",
        "location_country": "India"
    },
    {
        "email": "sarah@example.com",
        "password": "password123",
        "gender": "female",
        "first_name": "Sarah",
        "last_name": "Williams",
        "date_of_birth": "1991-08-25",
        "height": 168.0,
        "religion": "Christian",
        "marital_status": "never_married",
        "occupation": "Teacher",
        "education": "Bachelor's Degree",
        "location_city": "Chennai",
        "location_state": "Tamil Nadu",
        "location_country": "India"
    }
]

# Insert test users
for user in test_users:
    # Check if user already exists
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (user["email"],))
    if cursor.fetchone() is None:
        # Insert user
        cursor.execute(
            "INSERT INTO users (email, password_hash, profile_complete, account_status, registration_date, last_login) VALUES (?, ?, ?, ?, ?, ?)",
            (user["email"], hash_password(user["password"]), True, "active", datetime.now().isoformat(), datetime.now().isoformat())
        )
        user_id = cursor.lastrowid
        
        # Insert user profile
        cursor.execute(
            """
            INSERT INTO user_profiles (
                user_id, first_name, last_name, gender, date_of_birth, height, religion, 
                marital_status, occupation, education, location_city, location_state, location_country
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, user["first_name"], user["last_name"], user["gender"], user["date_of_birth"], 
                user["height"], user["religion"], user["marital_status"], user["occupation"], 
                user["education"], user["location_city"], user["location_state"], user["location_country"]
            )
        )
        
        # Insert match preferences
        min_age = 25 if user["gender"] == "male" else 25
        max_age = 35 if user["gender"] == "male" else 40
        height_min = 160 if user["gender"] == "male" else 170
        height_max = 175 if user["gender"] == "male" else 190
        
        cursor.execute(
            """
            INSERT INTO match_preferences (
                user_id, min_age, max_age, height_min, height_max, religion
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, min_age, max_age, height_min, height_max, user["religion"])
        )
        
        # Insert family details
        cursor.execute(
            """
            INSERT INTO family_details (
                user_id, father_occupation, mother_occupation, siblings_count, family_type, family_values
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, "Business", "Homemaker", 1, "nuclear", "traditional")
        )
        
        print(f"Added user: {user['first_name']} {user['last_name']} ({user['email']})")
    else:
        print(f"User {user['email']} already exists")

# Create some connections between users
connections = [
    {"sender": "john@example.com", "receiver": "jane@example.com", "status": "accepted"},
    {"sender": "michael@example.com", "receiver": "sarah@example.com", "status": "pending"}
]

for connection in connections:
    # Get user IDs
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (connection["sender"],))
    sender_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (connection["receiver"],))
    receiver_id = cursor.fetchone()[0]
    
    # Check if connection already exists
    cursor.execute(
        "SELECT connection_id FROM connections WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)",
        (sender_id, receiver_id, receiver_id, sender_id)
    )
    
    if cursor.fetchone() is None:
        # Insert connection
        cursor.execute(
            "INSERT INTO connections (sender_id, receiver_id, status, connection_date, last_updated) VALUES (?, ?, ?, ?, ?)",
            (sender_id, receiver_id, connection["status"], datetime.now().isoformat(), datetime.now().isoformat())
        )
        print(f"Added connection: {connection['sender']} -> {connection['receiver']} ({connection['status']})")
    else:
        print(f"Connection between {connection['sender']} and {connection['receiver']} already exists")

# Create some messages
messages = [
    {"sender": "john@example.com", "receiver": "jane@example.com", "text": "Hi Jane, I liked your profile!"},
    {"sender": "jane@example.com", "receiver": "john@example.com", "text": "Thank you, John! I liked yours too."}
]

for message in messages:
    # Get user IDs
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (message["sender"],))
    sender_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (message["receiver"],))
    receiver_id = cursor.fetchone()[0]
    
    # Insert message
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, message_text, sent_date) VALUES (?, ?, ?, ?)",
        (sender_id, receiver_id, message["text"], datetime.now().isoformat())
    )
    print(f"Added message: {message['sender']} -> {message['receiver']}")

# Create a success story
cursor.execute("SELECT user_id FROM users WHERE email = ?", ("john@example.com",))
user1_id = cursor.fetchone()[0]

cursor.execute("SELECT user_id FROM users WHERE email = ?", ("jane@example.com",))
user2_id = cursor.fetchone()[0]

# Check if success story already exists
cursor.execute("SELECT story_id FROM success_stories WHERE user_id = ? AND partner_id = ?", (user1_id, user2_id))
if cursor.fetchone() is None:
    # Insert success story
    cursor.execute(
        """
        INSERT INTO success_stories (
            user_id, partner_id, story_title, story_content, wedding_date, story_date, is_featured, is_approved
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user1_id, user2_id, "Found my soulmate!", 
            "We met through this platform and instantly connected. After a few months of getting to know each other, we decided to get married.",
            (datetime.now() + timedelta(days=30)).date().isoformat(), datetime.now().isoformat(), True, True
        )
    )
    print("Added success story")
else:
    print("Success story already exists")

# Commit changes and close connection
conn.commit()
conn.close()

print("Test data has been successfully added to the database!")


