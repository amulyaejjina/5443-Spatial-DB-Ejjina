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


@app.get("/findAll")
async def airports():
    sql = "SELECT * FROM public.airports limit 10"

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()


@app.get("/findOne/{country}")
async def airports(country):
    sql = f"""SELECT * FROM public.airports 
              WHERE country = '{country}'"""

    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        return cur.fetchall()


@app.get("/findClosest")
async def airports(city):
    sql_to_get_longlat = f"""SELECT lon,lat FROM AIRPORTS WHERE city = '{city}' """
    
    with DatabaseCursor("config.json") as cur:
        # First take the city entered by user 
        # and get the longitude and latitude
        # store it in variables
        cur.execute(sql_to_get_longlat)
        lon,lat = cur.fetchone()

        # Below query is main query to get closest neighbours
        sql = f"""SELECT *,ST_Distance('SRID=4326;POINT({lon} {lat})',geom) AS dist
        FROM public.airports
        ORDER BY dist LIMIT 10;"""
        cur.execute(sql)
        return cur.fetchall()

#-------------------------   QUERIES FOR POSTGRES SETUP   ----------------------
# CREATE TABLE,LOAD TABLE,LOAD LOCATION FROM LON,LAT


# To guide search
path = """SET search_path TO public;"""

# One time step
create_extension = """CREATE EXTENSION postgis;"""

# drop the table if already exists
drop_table = "DROP TABLE  IF EXISTS public.airports;"

# To create a table with necessary columns
create_table = """CREATE TABLE airports (
    id NUMERIC,
    name VARCHAR(100) NOT NULL,

    city VARCHAR(64) NOT NULL,
    country VARCHAR(256) NOT NULL,
    _3code VARCHAR(3) NOT NULL,
    _4code VARCHAR(4) NOT NULL,
    lat double precision NOT NULL,
    lon double precision  NOT NULL,
    elevation VARCHAR(10),
    gmt VARCHAR(10),
    tz_short VARCHAR(3),
    time_zone VARCHAR(64),
    type VARCHAR(32),
    type2 VARCHAR(32),
    geom GEOMETRY(POINT, 4326));"""

# To load airports.csv data into the created table
load_table = """COPY airports (
        id,name,city,country,_3code,_4code,
        lat,lon,elevation,gmt,tz_short,time_zone,
        type,type2
    ) FROM '/Users/amulyaejjina/Documents/5443-Spatial-DB-Ejjina/airports.csv' WITH CSV HEADER;
"""

# To upadate the 'geom' column with longitude,latitude
load_location = """UPDATE airports
SET geom = ST_SetSRID(ST_MakePoint(lon,lat), 4326);
"""

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