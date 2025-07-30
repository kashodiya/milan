



import sqlite3

# Connect to the database
conn = sqlite3.connect('matrimonial.db')  # This will use the database in the current directory (backend/)
cursor = conn.cursor()

# Check if tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Close the connection
conn.close()



