'''
Amulya Ejjina
Project 1
Description : Connect to PostGreSQL using psycopg2 module 
and using FastAPI
A local api that connects to the database with following routes:
    findAll
    findOne
    findClosest
'''

# Libraries for FastAPI
from lib2to3.pytree import convert
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

import psycopg2
import json
import csv

'''
Class name - DatabaseCursor
Purpose    - Used to connect to PostGreSQL through psycopg2 module

The connect() function of psycopg2 creates a new database session and returns 
a new instance of the connection class. By using the connection object, 
you can create a new cursor to execute any SQL statements.

'''
class DatabaseCursor(object):

    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):

        # Connecting to DB using psycopg2 connect method
        self.conn = psycopg2.connect(
            "dbname='"
            + self.conn_config["dbname"]
            + "' "
            + "user='"
            + self.conn_config["user"]
            + "' "
            + "host='"
            + self.conn_config["host"]
            + "' "
            + "password='"
            + self.conn_config["password"]
            + "' "
            + "port="
            + self.conn_config["port"]
            + " "
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):

        # some logic to commit/rollback
        self.conn.commit()
        self.conn.close()


# To guide search
path = """SET search_path TO public;"""

# Basic select queries 
airportquery = """SELECT *,geom::json FROM public.airports limit 5 ;"""
milbasesquery = """SELECT *,geom::json FROM public.milbases limit 5 ;"""
primaryroadsquery = """SELECT *,geom::json FROM public.primaryroads limit 5 ;"""
railroadsquery = """SELECT *,geom::json FROM public.railroads limit 5 ;"""
statesquery = """SELECT *,geom::json FROM public.states limit 5 ;"""
timezonesquery = """SELECT *,geom::json FROM public.timezones limit 5 ;"""

list = [airportquery,milbasesquery,primaryroadsquery,
railroadsquery,statesquery,timezonesquery]
#-------------------------   main   ----------------------------------

if __name__ == "__main__":
    with DatabaseCursor("config.json") as cur:

        # Iterating through a list of queries and executing each of them in loop
        # The below displays 5 rows of each table to terminal
        cur.execute(path)
        for item in list:
            cur.execute(item)
            data = cur.fetchall()
            print(data)
            # for row in data:
            #     print(row[0], )
            #     print(row[1],)
            #     print(row[2],)
            #     print(row[3],)
            #     print(row[4], )
            #     if not  str(item) == str(primaryroadsquery):
            #         print(row[5],)
            #     if str(item) == str(airportquery):
            #         print("Geometry  = ", json.dumps(row[15],indent=2))
            #     if str(item) == str(milbasesquery):
            #         print("Geometry  = ", json.dumps(row[10],indent=2))
            #     if str(item) == str(primaryroadsquery):
            #         print("Geometry  = ", json.dumps(row[6],indent=2))
            #     if str(item) == str(railroadsquery):
            #         print("Geometry  = ", json.dumps(row[5],indent=2))
            #     if str(item) == str(statesquery):
            #         print("Geometry  = ", json.dumps(row[16],indent=2))
            #     if str(item) == str(timezonesquery):
            #         print("Geometry  = ", json.dumps(row[17],indent=2))
            #     print("\n-----------------------------------------")


# ---------------------   END OF PROGRAM   ----------------------------