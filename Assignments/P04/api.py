import math
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import psycopg2
import json
import random
import geopandas as gpd
from geojson import Point, Feature, FeatureCollection, dump
from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2
import time
from threading import Thread
from datetime import datetime
from globals import *
import asyncio
from pydantic import BaseModel
from datetime import datetime, timezone

"""
           _____ _____   _____ _   _ ______ ____
     /\   |  __ \_   _| |_   _| \ | |  ____/ __ \
    /  \  | |__) || |     | | |  \| | |__ | |  | |
   / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
  / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
 /_/    \_\_|   |_____| |_____|_| \_|_|    \____/

The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
"""

# description = """🚀
# ## 🚀Missile Command🚀
# ### But Not Really
# """
# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="🚀Missile Command🚀",
    version="0.0.1",
    terms_of_service="🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

"""
  ___   _ _____ _
 |   \ /_\_   _/_\
 | |) / _ \| |/ _ \
 |___/_/ \_\_/_/ \_\
"""

# stores defenders playing missile command
participants = {}
makePartSQL = "INSERT INTO public.participants VALUES ("

def makeParticipantTable(eachDefender):
    with DatabaseCursor('config.json') as cur:
        cur.execute(eachDefender)
        print('sql uploaded')

missile_data = {
    "missiles": {
        "Atlas": {"speed": 1, "blast": 7},
        "Harpoon": {"speed": 2, "blast": 8},
        "Hellfire": {"speed": 3, "blast": 7},
        "Javelin": {"speed": 4, "blast": 7},
        "Minuteman": {"speed": 5, "blast": 9},
        "Patriot": {"speed": 6, "blast": 6},
        "Peacekeeper": {"speed": 7, "blast": 6},
        "SeaSparrow": {"speed": 8, "blast": 5},
        "Titan": {"speed": 8, "blast": 5},
        "Tomahawk": {"speed": 9, "blast": 6},
        "Trident": {"speed": 9, "blast": 9},
    },
    "speed": {
        1: {"ms": 111, "mph": 248.307},
        2: {"ms": 222, "mph": 496.614},
        3: {"ms": 333, "mph": 744.921},
        4: {"ms": 444, "mph": 993.228},
        5: {"ms": 555, "mph": 1241.535},
        6: {"ms": 666, "mph": 1489.842},
        7: {"ms": 777, "mph": 1738.149},
        8: {"ms": 888, "mph": 1986.456},
        9: {"ms": 999, "mph": 2234.763},
    },
    "blast": {1: 200, 2: 300, 3: 400, 4: 500, 5: 600, 6: 700, 7: 800, 8: 900, 9: 1000},
}


class DatabaseCursor(object):
    """https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    """

    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):
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


class DBQuery(object):
    def __init__(self, config):
        self.result = {}
        self.config = config
        self.limit = 1000
        self.offset = 0

    def __query(self, sql, qtype=3):
        with DatabaseCursor("config.json") as cur:
            #print(sql)
            cur.execute(sql)

            if qtype == 1:
                self.result["data"] = cur.fetchone()
            elif qtype == 2:
                self.result["data"] = cur.fetchmany()
            else:
                self.result["data"] = cur.fetchall()

            self.result["limit"] = self.limit
            self.result["offset"] = self.offset
            self.result["sql"] = sql
            self.result["success"] = cur.rowcount > 0
            self.result["effectedRows"] = cur.rowcount
        return self.result

    def queryOne(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}", 1)

    def queryAll(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(sql)

    def queryMany(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit
        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}")


conn = DBQuery("config.json")


"""
  _      ____   _____          _         _____ _                _____ _____ ______  _____
 | |    / __ \ / ____|   /\   | |       / ____| |        /\    / ____/ ____|  ____|/ ____|
 | |   | |  | | |       /  \  | |      | |    | |       /  \  | (___| (___ | |__  | (___
 | |   | |  | | |      / /\ \ | |      | |    | |      / /\ \  \___ \\___ \|  __|  \___ \
 | |___| |__| | |____ / ____ \| |____  | |____| |____ / ____ \ ____) |___) | |____ ____) |
 |______\____/ \_____/_/    \_\______|  \_____|______/_/    \_\_____/_____/|______|_____/
"""

# def dropRate(speed, distance, altitude):
#     time = distance / speed
#     return {"time": time, "rate": altitude / time}


class Position(object):
    def __init__(self, **kwargs):
        self.lon = kwargs.get("lon", 0.0)
        self.lat = kwargs.get("lat", 0.0)
        self.altitude = kwargs.get("altitude", 0.0)
        self.time = kwargs.get("time", 0.0)

    def __str__(self):
        lon = round(self.lon,4)
        lat = round(self.lon,4)
        alt = round(self.lon,4)
        time = round(self.lon,4)
        return f"{lon}, {lat}, {alt}, {time}"

class MissileInfo(object):
    @staticmethod
    def missile(name):
        if not name in list(missile_data["missiles"].keys()):
            return {"error": "Missile doesn't exist."}
        data = missile_data["missiles"][name]
        speed = missile_data["speed"][data["speed"]]
        blast = missile_data["blast"][data["blast"]]
        return {"speed": speed, "blast": blast}

    @staticmethod
    def blast(id):
        return missile_data["speeds"][id]

    @staticmethod
    def speed(id):
        return missile_data["blasts"][id]

class Participant:
    def __init__(self, id,active = False):
        global makePartSQL
        makePartSQL += f"{id}, "
        self.id = id
        self.region = self.assign_region()
        self.arsenal = self.assign_arsenal() 
        self.cities = self.assign_cities()
        self.active = active
        makePartSQL += f""" {self.active});"""
        makeParticipantTable(makePartSQL)
        makePartSQL = "INSERT INTO public.participants VALUES ("
        
    
    def assign_region(self):
        #returns region id, and region object
        return get_region(self.id)

    def assign_cities(self):
        with DatabaseCursor("config.json") as cur:
            geom = f"""SELECT newgeom from public.regions_simple WHERE cid = {self.id} AND gid = 6"""
            cur.execute(geom)
            region = cur.fetchall()[0][0]
            global makePartSQL

            sql = f"""SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(ST_AsGeoJSON(t.*)::json)
            )
            FROM public.cities as t(id, latitude, longitude, location) WHERE ST_INTERSECTS(location, '{region}');"""

            cur.execute(sql)
            sql3= cur.fetchall()[0][0]
            makePartSQL += f""" '{json.dumps(sql3)}', """

            # features = []
            # features.append(sql3)
            # feature_collection = FeatureCollection(sql3)

            # fc = {
            #     "type": "FeatureCollection",
            #     "features": feature_collection
            # }
            # feature = {
            # "type": "Feature",
            # "properties": {},
            # "geometry": {
            #     "type": None
            # }
            # }
            return sql3

    def assign_arsenal(self):
        return getArsenal(self.id)
    
class MissileServer(object):
    def __init__(self):
        #assigning the function to variable, so wheever someone calls 
        #missile server's clock , they get the system time
        self.clock = datetime.now()
        #self.backend_main_thread = Thread(target = self.main_thread)
        #start the backend_main_thread
        #self.backend_main_thread.start()
         #counter for missile id
        self.missile_counter = 1

    def main_thread(self):                
        print('thread pulsed')
        self.create_missiles()
        # check if any missile hit happened by now using clock
        self.check_deactivated_missiles()
        # increment clock - not needed as we are using system clock
        
    
   
    def create_missiles(self):
        ''' for every region, randomly chose a city
            and chose an initial point such that distance from target is over threshold
            (get that threshold from globals)
            chose a missile
            write to db
        '''
        # Bounding box geometry is stored in 'regions_simple' table with gid-10 and cid =10
        # (we are only using gid = 6 for region assignment since we have 6 teams)
        
        # The below will extract boundary and returns it
        # with DatabaseCursor("config.json") as cur:
        #     result = f"""SELECT ST_AsText(ST_Boundary(newgeom)) AS boundaryOfUSA FROM public.regions_simple where gid=10 AND cid=10"""
        #     cur.execute(result)
        #     getBoundary = cur.fetchall()
        #     # getBondary will return the US bbox's boundary in LINESTRING format
        #     return getBoundary

        # Loop for 6 iterations (this loop has to run every MISSILE_GEN_INTERVAL)
        global participants
        directions = ["East","West","North","South"]
        with DatabaseCursor("config.json") as cur:
            cur.execute("SELECT cities FROM public.participants WHERE active = True")
            activeParticipants = cur.fetchall()
        for eachDefender in activeParticipants:
            cityList = eachDefender[0]['features']
            targetCity = random.choices(cityList)[0]
            direct = random.choice(directions)

            # keep repeating till we find one such startpoint
            with DatabaseCursor("config.json") as cur:
                startLoc = self.randomStartPoint(direct)
                startLoc_lon = startLoc[0]
                startLoc_lat = startLoc[1]

                targetCity_lon = targetCity['geometry']['coordinates'][0]
                targetCity_lat = targetCity['geometry']['coordinates'][1]

                # Use ST_Distance to check distance btw target and start point
                query1 = f"""SELECT ST_Distance(
                    'SRID=4326;POINT({startLoc_lon} {startLoc_lat})'::geometry,
                    'SRID=4326;POINT({targetCity_lon} {targetCity_lat})'::geometry);"""
                cur.execute(query1)
                distance = cur.fetchall()[0][0]

                # Data for INSERTS
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                start_time = current_time
                
                altitude = random.randrange(10000,15000,300)

                startPoint = Position(lon=startLoc_lon, lat=startLoc_lat, altitude=altitude, time=1)
                targetPoint = Position(lon=targetCity_lon, lat=targetCity_lat, altitude=0, time=4)
                bearing = compass_bearing(startPoint, targetPoint)

                listofMissiles = list(missile_data['missiles'].keys())
                missileType = random.choices(listofMissiles)
                speedinmph = missile_data["speed"][missile_data["missiles"][missileType[0]]["speed"]]['ms']

                findtargetID = f"""SELECT id FROM public.cities
                WHERE longitude = {targetCity_lon} AND latitude = {targetCity_lat};"""
                cur.execute(findtargetID)
                targetID = cur.fetchall()[0][0]

                totalDistance = haversineDistance(startLoc_lon,startLoc_lat,targetCity_lon,targetCity_lat,"meters")
                totalTime = (totalDistance/speedinmph)/60

                mistype = missileType[0]
                # have to insert bearing - right now I dont see a column in db
                sql = f"""INSERT INTO missile_data VALUES ({self.missile_counter}, '{current_time}',
                'SRID=4326;POINT({startLoc_lon} {startLoc_lat})'::geometry, {targetID},
                'SRID=4326;POINT({targetCity_lon} {targetCity_lat})'::geometry, '{start_time}',
                'SRID=4326;POINT({startLoc_lon} {startLoc_lat})'::geometry, {speedinmph},
                {altitude}, {speedinmph}, true,{bearing},'{mistype}');"""
                cur.execute(sql)
                print('missile was inserted')
                self.missile_counter += 1


                    
    def updateCurrentMissiles(self):
        '''
        1. Fetch all rows from missile_data table
        2. For each row,get current required columns
        3. Calculations
        4. Update same row with calculated current values
        5. Repeat samew for all rows
        '''
        # Format of rows fetched fromt table - [(),(),()]
    
        with DatabaseCursor("config.json") as cur:
            getTable = f"""SELECT * FROM public.missile_data;"""
            cur.execute(getTable)
            missileList = cur.fetchall()

            ''' for each row,update the required columns -
            1. current location
            2. current time
            3. altitude'''
            for eachrow in missileList:
                # the indexes has to be changed based on updated db cols
                id = eachrow[0]
                currentTime = eachrow[1]
                currentLoc=eachrow[2]
                targetID = eachrow[3]
                speed = eachrow[7]
                alt = eachrow[8]
                bearing = eachrow[11]
                droprate = eachrow[9]

                getlatlon = f"""SELECT ST_X(current_loc) as x , ST_Y(current_loc) as y 
                FROM public.missile_data
                WHERE missile_id={id};"""
                cur.execute(getlatlon)
                currentlon,currentlat = cur.fetchall()[0][0]

                # Find next location based on 1 sec time elapsed assumption
                # returns a point geometry,assuming drop rate  -100m/sec
                nextPoint = nextLocation(currentlon, currentlat, speed, bearing)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                with DatabaseCursor("config.json") as cur:
                    updatesql = f"""UPDATE public.missile_data
                    SET current_loc = {nextPoint},current_time='{current_time}'
                    ,altitude= {alt - droprate}
                    WHERE missile_id = {id};"""
                    cur.execute(updatesql)
        

    def randomStartPoint(self, side):
        """Generates a random lon/lat on a predefined bounding box."""
        top = 54.3457868
        left = -129.7844079
        right = -61.9513812
        bottom = 19.7433195

        xRange = abs(left) - abs(right)
        yRange = abs(top) - abs(bottom)
        
        if side in "North":
            return [-(random.random()+1) * xRange, top]
        if side in "South":
            return [-(random.random()+1) * xRange, bottom]
        if side in "East":
            return [right, (random.random()+0.5) * yRange]
        if side in "West":
            return [left, (random.random()+0.5) * yRange]

    def check_deactivated_missiles(self):
        # run a query to get all missiles that have predicted hit time < current clock time
        # update their status to de-activated
        pass

    def radar_sweep(self):
        #missileserver.create_missiles()
        with DatabaseCursor("config.json") as cur:
            query = """SELECT jsonb_build_object(
                        'type',     'FeatureCollection',
                        'features', jsonb_agg(features.feature)
                    )
                    FROM (
                    SELECT jsonb_build_object(
                        'type',       'Feature',
                        'id',         missile_id,
                        'geometry',   ST_AsGeoJSON(current_loc)::jsonb,
                        'properties', to_jsonb(inputs) - 'missile_id' - 'current_loc' - 'target_id' - 'target_city' - 'active' - 'start_time' - 'start_loc' -'speed' - 'drop_rate'
                    ) AS feature
                    FROM (SELECT * FROM public.missile_data WHERE active = true) inputs) features;"""

            #Get column names of the missile data
            cur.execute(query)
            missiles = cur.fetchall()[0][0]

            #Show column name along with the missile's values if we have missile to show
            if(missiles['features'] != None):
                return missiles
            else:
                return {"N/A" : "No missiles are flying over the USA at this time"}
        
    def fired_solutions(self, solution_data):
        curr_time = self.clock()
        # read in the team id, missile type, targeted missile id , start location , fired direction and start time
        # get targetted missile data from table using targetted missile id from above
        # calculate intersection point using postgis api
        # calculate the time taken by our missile to reach there (time_taken)
        # calculate their missile's location by that time (by curr_time + time_taken)
        # if the difference between this location and the intersection point is less than blast radius,
            #  update our missile table with blast_time = curr_time + time_taken 
        # else:
            # dont update anything, or maintain a separate table for failed missiles if we want to send a notification after some time.

        # decrement the missile based on missile_type from team_id's arsenal

    def registerDefender(self, id):
        participants[id] = Participant(id)
        #makeParticipantTable(id)
        return participants[id].__dict__

def dsba(pos1, pos2):
    """
    Params:
        pos1 (Position) : lon,lat,altitude,time
        pos2 (Position) : lon,lat,altitude,time
    Returns:
        distance: in meters
        speed: in meters per second
        bearing: degrees where 90=east and 270=west
        dropRate: where I calculate the drop rate of the missile
    """

    bearing = compass_bearing(pos1, pos2)
    distance = haversineDistance(pos1.lon,pos1.lat,pos2.lon,pos2.lat,"meters")
    timeDiff = abs(pos1.time-pos2.time)
    altDiff = pos1.altitude-pos2.altitude
    speed = distance * timeDiff
    dropRate = altDiff / timeDiff

    d = round(distance,2)
    s = round(speed,2)
    b = round(bearing,2)
    a = round(dropRate,2)
    return {"distance":d,"speed":s,"bearing":b,"dropRate":a}

def haversineDistance(lon1, lat1, lon2, lat2, units="meters"):
    """Calculate the great circle distance in kilometers between two points on the earth (start and end) where each point
        is specified in decimal degrees.
    Params:
        lon1  (float)  : decimel degrees longitude of start (x value)
        lat1  (float)  : decimel degrees latitude of start (y value)
        lon2  (float)  : decimel degrees longitude of end (x value)
        lat3  (float)  : decimel degrees latitude of end (y value)
        units (string) : miles or km depending on what you want the answer to be in
    Returns:
        distance (float) : distance in whichever units chosen
    """
    radius = {"km": 6371, "miles": 3956,"meters": 6371000,"feet":20887680}

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = radius[units]  # choose miles or km for results

    return c * r

def compass_bearing(PositionA, PositionB):
    """Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    Source:
        https://gist.github.com/jeromer/2005586
    Params:
        pointA  : The tuple representing the latitude/longitude for the first point. Latitude and longitude must be in decimal degrees
        pointB  : The tuple representing the latitude/longitude for the second point. Latitude and longitude must be in decimal degrees
    Returns:
        (float) : The bearing in degrees
    """

    if not isinstance(PositionA, Position) or not isinstance(PositionB, Position):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(PositionA.lat)
    lat2 = radians(PositionB.lat)

    diffLong = radians(PositionB.lon - PositionA.lon)

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    # convert to radians
    compass_bearing = compass_bearing  * (math.pi/180)
    return compass_bearing

def getArsenal(id):
    """ Returns a missile arsenal randomly generated weighted to 
        give more slower weaker missiles that fast and strong.
    Params:
        id : id of the team 
        total (int) : total number of missiles to be issued
    """
    #TODO : do something here
    total = 100
    names = list(missile_data["missiles"].keys())

    missiles = []


    i = len(names)*2
    for name in sorted(names):
        #print(name,i)
        missiles.extend([name] * i)
        #print(len(missiles))
        i -= 2

    random.shuffle(missiles)

    missileCount = {}

    sum = 0
    for name in names:
        missileCount[name] = missiles[:total].count(name)
        
        if missileCount[name] == 0:
            missileCount[name] += 1
            missileCount["Atlas"] -= 1

        sum += missileCount[name] 
        
    missileCount['total'] = sum
    global makePartSQL
    makePartSQL += f""" '{json.dumps(missileCount)}', """
    return missileCount

    return feature_collection

def get_region(id:int):
    sql = f"""SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', json_agg(ST_AsGeoJSON(t.*)::json)
            )
            FROM public.regions_simple as t(gid, cid, newgeom) WHERE t.cid = {id} AND t.gid = 6;"""
    features = []
    with DatabaseCursor("config.json") as cur:
        cur.execute(sql)
        sql3= cur.fetchall()[0][0]
        global makePartSQL
        makePartSQL += f""" '{json.dumps(sql3)}', """
        return sql3

def nextLocation(lon: float, lat: float, speed: float, bearing: float, time:int=1, geojson: int=0):
    """
    lon (float) : x coordinate
    lat (float) : y coordinate
    speed (int) : meters per second
    bearing (float) : direction in degrees (0-360)
    geojson(bool) : return the next position as a geojson object
    """
    if not geojson:
        select = "st_x(p2) as x,st_y(p2) as y"
    else:
        select = "ST_AsGeoJSON(p2)"
    with DatabaseCursor("config.json") as cur:
        sql = f"""
        WITH 
            Q1 AS (
                SELECT ST_SetSRID(ST_Project('POINT({lon} {lat})'::geometry, {speed*time}, radians({bearing}))::geometry,4326
                
                ) as p2
            )
    
        SELECT {select}
        FROM Q1
        """
        cur.execute(sql)
        return cur.fetchall()

def missilePath(d: str = None, buffer: float = 0):
    bbox = {
        "l": -124.7844079,  # left
        "r": -66.9513812,  # right
        "t": 49.3457868,  # top
        "b": 24.7433195,  # bottom
    }

    directions = ["N", "S", "E", "W"]

    if not d:
        d = random.shuffle(directions)

    x1 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    x2 = ((abs(bbox["l"]) - abs(bbox["r"])) * random.random() + abs(bbox["r"])) * -1
    y1 = (abs(bbox["t"]) - abs(bbox["b"])) * random.random() + abs(bbox["b"])
    y2 = (abs(bbox["t"]) - abs(bbox["b"])) * random.random() + abs(bbox["b"])

    if d == "N":
        start = [x1, bbox["b"] - buffer]
        end = [x2, bbox["t"] + buffer]
    elif d == "S":
        start = [x1, bbox["t"] + buffer]
        end = [x2, bbox["b"] - buffer]
    elif d == "E":
        start = [bbox["l"] - buffer, y1]
        end = [bbox["r"] + buffer, y2]
    else:
        start = [bbox["r"] + buffer, y1]
        end = [bbox["l"] - buffer, y2]

    return [start, end]



"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/

 This is where your routes will be defined. Remember they are really just python functions
 that will talk to whatever class you write above. Fast Api simply takes your python results
 and packagres them so they can be sent back to your programs request.
"""
#this is needed here because I get errors when making it an instance in main --Ally
missileserver = MissileServer()

@app.get("/")
def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

stuff_lock = asyncio.Lock()
@app.get("/bg")
async def background():
    async with stuff_lock:
        missileserver.main_thread()
        await asyncio.sleep(MISSILE_GEN_INTERVAL)
        return {}


@app.get("/REGISTER")
async def register_user():
    # write a logic to find a unique id
    if(len(participants) < 6):
        id = random.randint(0, 5)
        while id in participants.keys():
            id = random.randint(0, 5)

        return missileserver.registerDefender(id)

    else:    
        return {'Error': 'No more regions available'}

@app.get("/START/{teamID}")
async def start(teamID):
    # Making the team active so that they get missiles
    alter = f"UPDATE public.participants SET active= true WHERE id= {int(teamID)}"
    try:
        with DatabaseCursor("config.json") as cur:
            cur.execute(alter)
            return {"Let get started !!! Use RADAR_SWEEP to see incoming missiles..."}

    except Exception as e:
        print(e)
        return {'Internal Error. Try calling the route one more time'}

@app.get("/RADAR_SWEEP")
async def radar_sweep():
    return missileserver.radar_sweep()

#@app.get("/missileInfo")
def missileInfo(name: str):
    return MissileInfo.missile(name)

class fireSol(BaseModel):
    team_id:  int
    target_missile_id: int
    missile_type: str 
    fired_time: str  
    firedfrom_lat: float
    firedfrom_lon: float 
    aim_lat: float 
    aim_lon: float 
    expected_hit_time: str
    speed: float 
    target_alt: float 

@app.post("/FIRE_SOLUTION/")
async def receive_solution(ms:fireSol):
    #return missileserver.fired_solutions(solution_dict)
    return ms

@app.get("/GET_CLOCK")
def get_time():
    return {"time" : str(missileserver.clock())}

@app.get("/QUIT/{teamID}")
async def quit(teamID):
     # Making the team active so that they get missiles
    alter = f"UPDATE public.participants SET active = True WHERE id = {int(teamID)}"
    try:
        with DatabaseCursor("config.json") as cur:
            cur.execute(alter)
            return {'Finished':'Your team has quit the game...'}

    except Exception:
        return {'Error' : 'Try quitting the game again'}

@app.get("/RESET")
def reset():
    """
    DO NOT call this method except for testing purposes. This will delete all missiles currently in the missile_data
    database and reset the registration assignment for a new game.
    """
    global participants
    participants = {}   #Reset all the regions to allow new participants to obtain a region

    missileserver.missile_counter = 1

    with DatabaseCursor("config.json") as cur:

        #Remove all the rows within the missile_data table
        sql = f"""DELETE FROM public.missile_data;"""
        cur.execute(sql)
        #Remove all participant data from the participants table
        cur.execute("DELETE FROM public.participants;")

    return {'Finished':'Game has reset'}

"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

After it is running, copy paste this into a browser: http://127.0.0.1:8080 

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    #initializing missile server 
    #missileserver = MissileServer()
    uvicorn.run("api:app", host="0.0.0.0", port=8080, log_level="debug", reload=True)
   # print(MissileInfo.missile("Patriot"))

    A = Position(lon=-94, lat=35, altitude=13000, time=0)
    B = Position(lon=-112.5, lat=35, altitude=13000, time=1)
    C = Position(lon=-112, lat=35.5, altitude=12980, time=4)
    #print(compass_bearing(B, C))
    #print(dsba(C, B))
