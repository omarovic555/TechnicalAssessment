import unittest
import sqlite3
from facebook_scraper import get_posts
from fastapi import FastAPI
import uvicorn

router = FastAPI()

def create_database(conn):
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS facebookdata (id INTEGER PRIMARY KEY, text TEXT, time DATE, likes INTEGER, shares INTEGER, comments INTEGER)")
        print("Table created successfully")
    except sqlite3.Error as error:
        print("Error while creating table", error)
    finally:
        cur.close()

def connect_to_database(conn):
    try:
        conn = sqlite3.connect("facebookscrapeddata.db")
        print("Connected to database successfully")
    except sqlite3.Error as error:
        print("Error while connecting to database", error)
    return conn

def save_data(conn):
    try:
        cur = conn.cursor()
        for post in get_posts("GuinnessWorldRecords", pages=3):
            text = post['text']
            time = post['time']
            likes = post['likes']
            shares = post['shares']
            comments = post['comments']
            cur.execute("INSERT INTO facebookdata (text, time, likes, shares, comments) VALUES (?, ?, ?, ?, ?)", (text, time, likes, shares, comments))
        print("Data saved successfully")
        # Execute the SELECT query
        cur.execute("SELECT * FROM facebookdata")

# Fetch all rows
        rows = cur.fetchall()

# Loop through the rows and print them
        for row in rows:
         print(row)

    except sqlite3.Error as error:
        print("Error while saving data", error)
    finally:
        cur.close()

@router.get("/")
def root():
    conn = sqlite3.connect("facebookscrapeddata.db")
    create_database(conn)
    conn = connect_to_database(conn)
    save_data(conn)
    conn.close()

class TestDatabaseFunctions(unittest.TestCase):
    def test_create_database(self):
        conn = sqlite3.connect("facebookscrapeddata.db")
        create_database(conn)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='facebookdata';")
        table = cur.fetchone()
        self.assertEqual('facebookdata', table[0])
        cur.close()
        conn.close()

    def test_connect_to_database(self):
        conn = sqlite3.connect("facebookscrapeddata.db")
        conn = connect_to_database(conn)
        self.assertIsNotNone(conn)

    def test_save_data(self):
        conn = sqlite3.connect("facebookscrapeddata.db")
        save_data(conn)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM facebookdata")
        count = cur.fetchone()
        self.assertGreaterEqual(count[0], 3)
        cur.close()
        conn.close()

if __name__ == '__main__':
  unittest.main()
  uvicorn.run(router,port=8008,host="0.0.0.0")
  
  