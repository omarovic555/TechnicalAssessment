import unittest
import psycopg2
from facebook_scraper import get_posts 
from fastapi import FastAPI
import uvicorn


router  = FastAPI()
@router.get("/")  
async def root(): 
 def create_database(conn):
    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE DATABASE facebookscrapeddata")
        print("Database created successfully")
    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists")
    finally:
        cur.close()
    #    conn.close()

 def connect_to_database(conn):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="facebookscrapeddata",
            user="postgres",
            password="5555"
        )
        print("Connected to database successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to database", error)
    return conn

 def create_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE facebookdata (
                id serial PRIMARY KEY,
                text TEXT,
                time Date ,
                likes INTEGER,
                shares Integer ,
                comments Integer 
                
            )
        """)
        print("Table created successfully")
    except psycopg2.errors.DuplicateTable:
        print("Table already exists")
    finally:
        cur.close()
        conn.commit()

 conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="5555"
 )
 def SaveData():
  try:
    for post in get_posts('GuinnessWorldRecords', pages=3):
   
     text = post['text']
   
     time=post['time']
   
     likes=post['likes']
   
     shares=post['shares']
   
     comments=post['comments']
     cur = conn.cursor()
     cur.execute("INSERT INTO facebookdata (text, time,likes,shares,comments) VALUES (%s, %s, %s, %s, %s)", (text, time, likes, shares, comments))

    # Commit the changes to the database
     conn.commit()
     print("row inserted successfully")
  except: 
     print("row not inserted successfully")
  finally:
   # Close the cursor and connection
     cur.close()
 
 create_database(conn)
 conn = connect_to_database(conn)
 create_table(conn)
 SaveData()

#conn.close()
 class TestDatabaseFunctions(unittest.TestCase):
  def test_create_database(self):
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="5555"
        )
        create_database(conn)
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database")
        databases = cur.fetchall()
        self.assertIn(('facebookscrapeddata',), databases)
        cur.close()
        conn.close()

  def test_connect_to_database(self):
        connect_to_database(conn)
        self.assertIsNotNone(conn)

  def test_create_table(self):
        conn = psycopg2.connect(
            host="localhost",
            database="facebookscrapeddata",
            user="postgres",
            password="5555"
        )
        create_table(conn)
        cur = conn.cursor()
        cur.execute("SELECT relname FROM pg_class WHERE relkind='r' AND relname='facebookdata';")
        table = cur.fetchone()
        self.assertEqual('facebookdata', table[0])
        cur.close()
        conn.close()

  def test_SaveData(self):
        conn = psycopg2.connect(
            host="localhost",
            database="facebookscrapeddata",
            user="postgres",
            password="5555"
        )
        SaveData()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM facebookdata")
        count = cur.fetchone()
        self.assertGreaterEqual(count[0], 3)
        cur.close()
        conn.close()

 if __name__ == '__main__':
  unittest.main()
   
