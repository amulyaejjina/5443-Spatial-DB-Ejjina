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
from code import interact
from lib2to3.pytree import convert
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

import psycopg2
import json
import random
from geojson import Point, Feature, FeatureCollection, dump
from shapely.geometry import MultiPoint


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

def randomStartPoint(side):
        """Generates a random lon/lat on a predefined bounding box."""
        top = 54.3457868
        left = -129.7844079
        right = -61.9513812
        bottom = 19.7433195

        xRange = abs(left) - abs(right)
        yRange = abs(top) - abs(bottom)
        
        if side in "North":
            return [-random.random() * xRange, top]
        if side in "South":
            return [-random.random() * xRange, bottom]
        if side in "East":
            return [right, random.random() * yRange]
        if side in "West":
            return [left, random.random() * yRange]


def createMissilePathPointSet():
    directions = "East","West","North","South"
    pointSets=[]
    for i in range(2):
        dir = random.choice(directions)
        if dir == "East":
            pointSets.append([randomStartPoint(dir),randomStartPoint("West")])
        if dir == "West":
            pointSets.append([randomStartPoint(dir),randomStartPoint("East")])
        if dir == "North":
            pointSets.append([randomStartPoint(dir),randomStartPoint("South")])
        if dir == "South":
            pointSets.append([randomStartPoint(dir),randomStartPoint("North")])
    return pointSets


# To guide search
path = """SET search_path TO public;"""

# Basic select queries 

#-------------------------   main   ----------------------------------

if __name__ == "__main__":

    pointsets = createMissilePathPointSet()
    f = open("paths.geojson", "w")
    with DatabaseCursor("config.json") as cur:
        features = []
        for each in pointsets:
            interpolateQuery = """SELECT ST_AsGeoJSON
            (ST_LineInterpolatePoints('LINESTRING({} {},{} {})', 0.01))""".format(each[0][0],each[0][1],each[1][0],each[1][1])
    
            cur.execute(interpolateQuery)
            data = cur.fetchall()

            features.append(data)
        feature_collection = FeatureCollection(features)
        #print(feature_collection)

        with open('myfile.geojson', 'a') as f:
            dump(feature_collection, f)
# ---------------------   END OF PROGRAM   ----------------------------