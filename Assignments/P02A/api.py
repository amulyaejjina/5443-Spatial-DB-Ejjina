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


#---------------------------   FastAPI   --------------------------------
'''
The `description` is the information that gets displayed when the api is 
accessed from a browser and loads the base route.Also the instance of `app` 
below description has info that gets displayed 
as well when the base route is accessed.
'''
description = """🚀
## Api to interact with PostGreSQL
### Retrievs data from DB
"""

# Create a FastAPI "instance" from fastapi
app = FastAPI(
    title="Api to interact with PostGreSQL",
    description=description,
    version="0.0.1",
    terms_of_service="http://killzonmbieswith.us/worldleterms/",
    contact={
        "name": "Worldle Clone",
        "url": "http://killzonmbieswith.us/worldle/contact/",
        "email": "chacha@killzonmbieswith.us",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# ----------------------------  ROUTES -----------------------------------

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/airports")
async def airports():
    sql = "SELECT *,geom::json FROM public.airports limit 10;"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

@app.get("/milbases")
async def airports():
    sql = "SELECT *,geom::json FROM public.milbases limit 10;"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

@app.get("/primaryroads")
async def airports():
    sql = "SELECT *,geom::json FROM public.primaryroads limit 10;"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

@app.get("/railroads")
async def airports():
    sql = "SELECT *,geom::json FROM public.railroads limit 10;"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

@app.get("/states")
async def airports():
    sql = "SELECT *,geom::json FROM public.states limit 10;"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

@app.get("/timezones")
async def airports():
    sql = "SELECT *,geom::json FROM public.timezones limit 10;"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()

# To guide search
path = """SET search_path TO public;"""

#-------------------------   main   ----------------------------------

if __name__ == "__main__":
    with DatabaseCursor("config.json") as cur:
        cur.execute(path)

        '''Commenting below as its needed for only first load
           Will work uncommented too but its unnecessary loads.'''
        # cur.execute(create_extension)
        # cur.execute(drop_table)
        # cur.execute(create_table)
        # cur.execute(load_table)
        # cur.execute(load_location)

    uvicorn.run("api:app", host="0.0.0.0", port=8080, log_level="debug", reload=True)

# ---------------------   END OF PROGRAM   ----------------------------