import json
import psycopg2
from random import shuffle, randint
import math

"""             DATABASE CURSOR CLASS          """
class DatabaseCursor(object):

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
        self.conn.commit()
        self.conn.close()
"""--------------------------------END OF DATABASE CURSOR CLASS---------------------------------------------"""

#Get the upper and lower points of the given bounding box.
bbox = {
    "UpperLeft": {"lon": -10.31324002, "lat": 50.17116998},
    "LowerRight": {"lon": -8.06068579, "lat": 48.74631646},
}

#Get each type of sector that could possibly be given to us and hold them in a list
cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
        "S","SSW","SW","WSW","W","WNW","NW","NNW"]

#Look at ships for testing and checking
geojson = """{
"type": "FeatureCollection",
"features": [
    """
#Open database cursor to begin PostGIS functions and cutting out which sector of the bounding box we get
with DatabaseCursor("config.json") as cur:

    #Make the bounding box and store it as a polygon
    box = f"""SELECT ST_AsText(ST_MakeEnvelope(
                    {bbox['UpperLeft']['lon']}, {bbox['UpperLeft']['lat']},
                    {bbox['LowerRight']['lon']}, {bbox["LowerRight"]['lat']}
                    ));"""

    cur.execute(box)
    box = cur.fetchall()[0][0]

    #Store it as a geojson feature so I can look at it in qgis
    geojson += """{
            "type": "Feature",
            "properties": { },
            "geometry": {
            "type": "Polygon", 
                "coordinates": [
                ["""
    geo_box = box.strip("))")
    geo_box = geo_box.strip('POLYGON((')
    coordinates = geo_box.split(',')
    for coordinate in coordinates:
        x,y = coordinate.split()
        geojson += f"""[{x}, {y}],"""
    geojson = geojson[:-1]
    geojson += """]]}},"""

    #Shuffle the list of possible sectors and randomly grab one.
    #This is to ensure we do not hardcode anything in the moment
    shuffle(cardinalList)    
    cardinalSpot = cardinalList[0]

    #Based on which sector we get, grab the degrees that the sector is within in order to determine its boundary
    c_degrees = f"""SELECT start_degree, middle_degree, end_degree FROM cardinalDegrees WHERE direction = '{cardinalSpot}'"""
    cur.execute(c_degrees)
    start_degree, middle_degree, end_degree = cur.fetchall()[0]

    #Get the point in the center of the bounding box
    center_bbox = f"""SELECT ST_AsText(ST_Centroid('{box}'));"""
    cur.execute(center_bbox)
    center_point = cur.fetchall()[0][0]

    #Cut out and separate the sector that we were given from the bounding box,
    #this is done by getting the center of the bbox and using the start_degree and end_degree as bearing,
    #make two lines that pass through the bbox's bounds and essentially "cut out" the sector by splitting it
    #from the rest of the polygon using ST_Split. This returns a geometrycollection
    chopped_bbox = f"""SELECT ST_AsText(ST_Split(
                '{box}'::geometry,
                ST_MakeLine(
                    ST_MakeLine(ST_SetSRID(ST_Project('{center_point}'::geography, {200000}, RADIANS({start_degree}))::geometry, 0), '{center_point}')::geometry,
                    ST_MakeLine(ST_SetSRID(ST_Project('{center_point}'::geography, {200000}, RADIANS({end_degree}))::geometry,0), '{center_point}')::geometry
                    )));"""

    cur.execute(chopped_bbox)
    chopped_bbox = cur.fetchall()[0][0]

    #The sector is always the second geometry in the geometrycollection
    sector = f"""SELECT ST_AsText(ST_GeometryN('{chopped_bbox}', 2));"""
    cur.execute(sector)
    sector = cur.fetchall()[0][0]
    print(cardinalSpot)
    #print(sector)

    #Store sector as geojson feature so I can look at it in qgis
    geojson += """{
            "type": "Feature",
            "properties": { },
            "geometry": {
            "type": "Polygon", 
                "coordinates": [
                ["""
    geo_sector = sector.strip("))")
    geo_sector = geo_sector.strip('POLYGON((')
    coordinates = geo_sector.split(',')
    for coordinate in coordinates:
        x,y = coordinate.split()
        geojson += f"""[{x}, {y}],"""
    geojson = geojson[:-1]
    geojson += """]]}},"""


    ship_dicts = []
    with open("ships.json", "r") as myFile:
        ships = json.load(myFile)

        #Fill in the ship table with all of our ships' data

        cur.execute("""DELETE FROM public.gun_state; 
                       DELETE FROM public.ships_guns;
                       DELETE FROM public.ship_state;
                       DELETE FROM public.torpedo_state;
                       DELETE FROM public.ship; """)
        for ship in ships:
            count = 0
            insert = f"""INSERT INTO public.ship(ship_id, category, shipclass, length, width, torpedolaunchers, armament, armor, speed, turn_radius)
             VALUES (
                {ship["id"]}, '{ship["category"]}', '{ship["shipClass"]}',
              {ship["length"]}, {ship["width"]}, '{json.dumps(ship['torpedoLaunchers'])}', '{json.dumps(ship["armament"])}', '{json.dumps(ship["armor"])}', {ship["speed"]}, {ship["turn_radius"]});"""
            cur.execute(insert)
            ship_dicts.append({'ship_id' : ship["id"]})

            #Fill in the ship_guns table
            for weapon in ship['armament']:
                insert = f"""INSERT INTO public.ships_guns VALUES(
                    {ship["id"]}, {count}, '{weapon['gun']['name']}', {weapon['pos']});"""

                cur.execute(insert)

                #Fill in the initial state of the gun
                insert = f"""INSERT INTO public.gun_state VALUES(
                    {ship['id']}, {count}, 0, 0, {weapon['gun']['ammo'][0]['count']});"""
                cur.execute(insert)
                count += 1
            
            #Fill in the initial state of torpedo launchers if the ship has them
            if(ship["torpedoLaunchers"] is not None):
                t_count = 0
                for torpedo in ship["torpedoLaunchers"]:
                    insert = f"""INSERT INTO public.torpedo_state VALUES(
                       {ship["id"]},
                       {t_count},
                       {torpedo['torpedos']['speed']}, '{torpedo["location"]+", "+torpedo['side']+", "+ torpedo['facing']}',
                       '{torpedo['torpedos']['name']}'
                       );"""
                    cur.execute(insert)
                    t_count += 1
            
    inside = False
    while(inside is not True):
            
        #Pick a starting point within the sector for the center of the first ship
        random_start_point = f"""SELECT ST_AsText(ST_GeneratePoints('{sector}'::geometry, 1));"""
        cur.execute(random_start_point)
        random_start_point = cur.fetchall()[0][0]
        random_start_point = random_start_point[5:] #Remove MULTI FROM MULTIPOINT to make it just a POINT

        #Get the longitude and latitude of the random point
        xy = f"""SELECT ST_X('{random_start_point}'::geometry), ST_Y('{random_start_point}'::geometry);"""
        cur.execute(xy)
        random_start_x, random_start_y = cur.fetchall()[0]

        #Store all needed information for testing and output
        all_ships_centers = []  #center point of all of the ships
        all_shipgeoms = []      #geometry containing bbox of each ship
        all_ships = []          #polygon of each ship's bbox

        ##Get the dimensions of the first ship
        ship_1 = f"""SELECT length, width FROM public.ship LIMIT 1;"""
        cur.execute(ship_1)
        ship_y, ship_x = cur.fetchall()[0]

        #The first ship point is the center of the current ship
        current_ship_center = random_start_point

        #Determine how many ships needs to be in a single row
        x_distance_amount = math.ceil(math.sqrt(len(ships)))

        #the ships should be staggered for every row
        stagger = -1

        #get the dimensions of all the ships
        ships = f"""SELECT length, width FROM public.ship;"""
        cur.execute(ships)
        ships = cur.fetchall()
     
        for ship in range(0, len(ships), x_distance_amount):

            #Stagger the first ship in each row so the ones below are between the ones above
            #Middle of the ships would be 111m as it is half of 222m
            next_ship_center = f"""SELECT ST_AsText(
                ST_Project(
                    '{current_ship_center}'::geography, 111,
                        RADIANS({90 * stagger})
                    ));"""

            cur.execute(next_ship_center)
            current_ship_center = cur.fetchall()[0][0]

            #Go back and forth to implement the staggering
            stagger *= -1

            for i in range(x_distance_amount):
                try:
                    #Space each ship by 222m. Only store the centers of each ship's point
                    #This is done by getting half the length of 
                    #the current ship + 222m + half the length of the next ship
                    ship_num = ship + i
                    next_ship_center = f"""SELECT ST_AsText(
                        ST_Project(
                            '{current_ship_center}'::geography,
                             {(ship_y/2) + 222 + (ships[ship_num][0]/2)},
                              RADIANS(90)
                            ));"""

                    ship_y = ships[ship_num][0]
                    cur.execute(next_ship_center)
                    current_ship_center = cur.fetchall()[0][0]
                    #Store the each ship's center point in a list
                    all_ships_centers.append(current_ship_center)
                
                    #Get the upper left corner of the current ship given its dimensions
                    bbox_point_upperLeft = f"""ST_Project(ST_Project(
                            '{current_ship_center}'::geography, {ships[ship_num][1]/2}, Radians(0)
                            ), {ships[ship_num][0]/2}, Radians(270))"""

                    #Get the bottom right corner of the current ship given its dimensions
                    bbox_point_bottomRight = f"""ST_Project(ST_Project(
                            '{current_ship_center}'::geography, {ships[ship_num][1]/2}, Radians(180)
                            ), {ships[ship_num][0]/2}, Radians(90))"""

                    #Convert the two corner points into x and y coordinates
                    bbox_point_upperLeft_xy = f"""
                    ST_X({bbox_point_upperLeft}::geometry), ST_Y({bbox_point_upperLeft}::geometry)"""

                    bbox_point_bottomRight_xy = f"""
                    ST_X({bbox_point_bottomRight}::geometry), ST_Y({bbox_point_bottomRight}::geometry)"""

                    #Get the bbox of the current ship containing its proper size. Store it as a geometry
                    cur.execute(f"""SELECT ST_MakeEnvelope(
                            {bbox_point_upperLeft_xy}, {bbox_point_bottomRight_xy}
                            );""")

                    all_shipgeoms.append(cur.fetchall()[0][0])

                    #All ships should face to the right if in the west and left if in the east
                    #If it is directly north or south then they can face either direction
                    #This will be changed in the future to face toward the center of the field if there
                    #is time
                    bearing = 90 if 'W' in cardinalSpot else 270

                    ship_dicts[ship_num]["bearing"] = bearing
                    
                    #Get the longitude and latitude of the center point of the current ship
                    current_ship_center_xy = f"""SELECT
                    ST_X(
                        '{current_ship_center}'::geometry),
                    ST_Y(
                        '{current_ship_center}'::geometry)"""

                    cur.execute(current_ship_center_xy)
                    current_ship_center_lon, current_ship_center_lat = cur.fetchall()[0]
                    ship_dicts[ship_num]['location'] =\
                        {'lon' : current_ship_center_lon, 'lat' : current_ship_center_lat}
                    
                    ship_AsText = f"""SELECT ST_AsText('{all_shipgeoms[-1]}')"""
                    cur.execute(ship_AsText)
                    all_ships.append(cur.fetchall()[0][0])

                    #print('length:', ships[ship_num][0], 'width:', ships[ship_num][1])
                except Exception:
                    break

            #Go back to the first column and move down one row. Space each ship down
            # 111m from each other. We are at the center so we need to move down to the bottom of the ship one row above
            #and then move down 111m and lastly reach the center of the next ship by moving down half its width
            next_ship_row = f"""SELECT ST_AsText(
                ST_Project(
                    '{random_start_point}'::geography, {(ship_x/2) + 111 + (ships[ship][1]/2)}, RADIANS(180)
                    ));"""

            cur.execute(next_ship_row)
            current_ship_center = cur.fetchall()[0][0]

            #new row is the next starting point
            random_start_point = current_ship_center

        #Store all geometries of every ship into one single geometry
        all_boats = f"""SELECT ST_AsText(ST_UNION(ARRAY{all_shipgeoms}));"""
        cur.execute(all_boats)
        all_boats = cur.fetchall()[0][0]

        #Check to see if all of the ships remained in the sector. The starting point was close to the edge of the sector if false
        in_bounds = f"""SELECT ST_WITHIN(ST_GEOMFROMTEXT('{all_boats}'), ST_GEOMFROMTEXT('{sector}'));"""
        cur.execute(in_bounds)
        inside = cur.fetchall()[0][0]
        print(inside)
        #Continue looping until all ships were within our given sector. 
        #Due to the size of the ships being very small in respect to the sector, all ships will be contained after at few
        #runs at the very most. So far, it has taken 5 loops max to get a good point

    
    for polygon in all_ships:
        polygon = polygon.strip(')),')
        geojson += """{
            "type": "Feature",
            "properties": { "stroke": "#FFFFFF",
			"stroke-width": 2,
			"stroke-opacity": 1,
			"fill": "#FFFFFF",
			"fill-opacity": 0.5},
            "geometry": {
            "type": "Polygon", 
                "coordinates": [
                ["""
        polygon = polygon.strip("))")
        polygon = polygon.strip('POLYGON((')
        coordinates = polygon.split(',')
        for coordinate in coordinates:
            x,y = coordinate.split()
            geojson += f"""[{x}, {y}],"""
        geojson = geojson[:-1]
        geojson += """]]}},"""


    #Move all ship info into ship_state
    for ship in range(len(ship_dicts)):
        cur.execute(f"SELECT speed from public.ship WHERE ship.ship_id = {ship_dicts[ship]['ship_id']}")
        speed = cur.fetchall()[0][0]
        insert = f"""INSERT INTO ship_state VALUES(
            {ship_dicts[ship]["ship_id"]},
            {ship_dicts[ship]["bearing"]},
            {speed},
            '{json.dumps(ship_dicts[ship]['location'])}',
            '{all_ships[ship]}'
            ); """
        cur.execute(insert)

    geojson = geojson[:-1]
    with open("shipLocations.json", 'w') as f:
        f.write(geojson)
        
    outputFile = {'fleet_id' : "kraken", "ship_status" : ship_dicts}
    with open("final_output.json", 'w') as f:
        f.write(json.dumps(outputFile, indent=4))