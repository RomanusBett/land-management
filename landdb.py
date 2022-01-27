import sqlite3
conn = sqlite3.connect("lands.db")
cursor = conn.cursor()
query = """CREATE TABLE land(
    id integer PRIMARY KEY,
    owner text NOT NULL, 
    location text NOT NULL,
    contacts text NOT NULL
)"""
cursor.execute(query)