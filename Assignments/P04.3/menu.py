'''

! MENU SYSTEM FOR BATTLESHIP GAME !

This uses "Console Menu" to create a menu system for the game.

    1. The menu options to interact with the "game" are defined in this local file menu.json.
    2. Each item in the menu will match up to an api route, with exactly the same definitions 
    3. This create our own menu driven system, that incorporates the menu items and function handlers.

Url that this program talks to -  https://battleshipgame.fun:1234/docs 

Problem Statement:
Given:

A bounding box: bbox with upper left and lower right coordinates.
A json list of ships like this one: ships.json.
Determine how many ships are in your fleet (by counting them im ships.json).
Then generate a pseudo random location for each ship within a given bbox and at a specified "sector" within that bbox. You can acheive this by generating a single point pseudo-randomly, then placing your ships accordingly starting with that point.

Ship Location and Orientation:

Each ship should be facing the same direction.
Your ships should be spaced apart and staggered (see image below).
111m from port to starboard
222m from bow to stern
You can be +/- 5 meters
Depending on where your ships materialize, be cognizant of each of your ships bearings. You don't want to immediately start leaving the battle area (see image below)
The "sector" will be chosen via a cardinal direction.

Sectors:

Here are sectors listed out visually on a compass. 
Normally sectors would use a grid system, but what's the fun in giving you an even smaller bounding box to generate coordinates in.

'''
import sys,os
from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
import requests
import json
import psycopg2
from random import shuffle, randint
import math
import requests,time

"""------------- DATABASE CURSOR CLASS ------------"""

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

"""---------------   END OF DATABASE CURSOR CLASS  ----------------"""

credentials = {
    "id": 15,
    "name": "kraken",
    "regdate": 1669156402,
    "exchange": "battleship",
    "port": 5672,
    "host": "battleshipgame.fun",
    "password": "kX3aF8x5z0Sw",
    "hash": "32223921880817397656263709201856725525"
}

#Look at ships for testing and checking
geojson = """{
"type": "FeatureCollection",
"features": [
    """
ship_dicts = []
game_id = -1
bbox = {}
sector = ""
change = False

def input_handler(text):
    pu = PromptUtils(Screen())
    # PromptUtils.input() returns an InputResult
    result = pu.input(text)
    pu.println("\nYou entered:", result.input_string, "\n")
    pu.enter_to_continue()



def get_CurrentGames():
    #Get the game ids of all current games active when api is active
    try:
        all_games = []
        url = f"https://battleshipgame.fun:8080/current_games/?hash={credentials['hash']}"
        games = requests.get(url).json()['data']
        #print(games)
        for game in games:
            all_games.append(json.dumps(game, indent=4))
        return all_games

    except:
        return None

def Game_Choices():
    #pick a game from list of all current active games
    games_toPlay = get_CurrentGames()
    if(games_toPlay is None or "Not Found" in games_toPlay):
        #For the sake of testing the menu
        return ['Default: Select If No Games Are Available']
    else:
        #Display all available games
        return games_toPlay

def pick_Game(chosen_game):
    #pick a game from list of all current active games
    games_toPlay = get_CurrentGames()
    if(games_toPlay is None or "Not Found" in games_toPlay):
        #For the sake of testing the menu
        return -1
    else:
        #Display all available games
        #print(type(games_toPlay[0]))
        return json.loads(games_toPlay[chosen_game])['game_id']


def get_GameBounds():
    #A game was found and chosen
    if(game_id >0):
        #Get the upper and lower points of the given bounding box and our sector.
        url = f"https://battleshipgame.fun:8080/get_battle_location/?hash={credentials['hash']}&game_id={game_id}"
        game = requests.get(url).json()
        bbox = json.dumps(game['bbox'], indent = 4)
        section = json.dumps(game['section'], indent=4)

    #No active games so just use default
    else:
    #----------------------------TO BE REPLACED WITH API ONCE WE CAN-----------------------------
    # #Test bbox
        bbox = {
            "UpperLeft": {"lon": -10.31324002, "lat": 50.17116998},
            "LowerRight": {"lon": -8.06068579, "lat": 48.74631646},
        }

        #Get each type of sector that could possibly be given to us and hold them in a list
        cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
            "S","SSW","SW","WSW","W","WNW","NW","NNW"]
        shuffle(cardinalList)
        section = "N"

    
    return [bbox, section]

def get_Fleet():
    global ship_dicts 
    ship_dicts = []
    with DatabaseCursor('config.json') as cur:

        url = f"https://battleshipgame.fun:8080/generate_fleet/?fleetName=kraken&hash={credentials['hash']}"
        ships = requests.get(url).json()

        #Replace with url when it is ready
        with open("ships.json", "w") as myFile:
            myFile.write(json.dumps(ships, indent=4))

            #Fill in the ship table with all of our ships' data

        cur.execute("""DELETE FROM public.gun_state; 
                    DELETE FROM public.ships_guns;
                    DELETE FROM public.ship_state;
                    DELETE FROM public.torpedo_state;
                    DELETE FROM public.ship; """)
        for ship in ships:
            count = 0
            insert = f"""INSERT INTO public.ship(ship_id, identifier, category, shipclass, length, width, torpedolaunchers, armament, armor, speed, turn_radius)
            VALUES (
                {ship["id"]}, '{ship["identifier"]}', '{ship["category"]}', '{ship["shipClass"]}',
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

        return ships       

def generate_Fleet():
    #Get all ships in our fleet
    ships = get_Fleet()

    #Open database cursor to begin PostGIS functions and cutting out which sector of the bounding box we get
    with DatabaseCursor("config.json") as cur:
        global geojson
        global bbox
        global sector
        global ship_dicts
        
        if(bbox == {} or sector == ""):
            return

        bbbox = json.loads(bbox)
        section = sector.strip('"')

        #Make the bounding box and store it as a polygon
        box = f"""SELECT ST_AsText(ST_MakeEnvelope(
                        {bbbox['UpperLeft']['lon']}, {bbbox['UpperLeft']['lat']},
                        {bbbox['LowerRight']['lon']}, {bbbox["LowerRight"]['lat']}
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

        #Based on which sector we get, grab the degrees that the sector is within in order to determine its boundary
        c_degrees = f"""SELECT start_degree, end_degree FROM cardinalDegrees WHERE direction = '{section}'"""
        cur.execute(c_degrees)
        #print(sector)
        start_degree, end_degree = cur.fetchall()[0]

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
        section = f"""SELECT ST_AsText(ST_GeometryN('{chopped_bbox}', 2));"""
        cur.execute(section)
        section = cur.fetchall()[0][0]
        #print(cardinalSpot)
        #print(sector)

        #Store sector as geojson feature so I can look at it in qgis
        geojson += """{
                "type": "Feature",
                "properties": { },
                "geometry": {
                "type": "Polygon", 
                    "coordinates": [
                    ["""
        geo_sector = section.strip("))")
        geo_sector = geo_sector.strip('POLYGON((')
        coordinates = geo_sector.split(',')
        for coordinate in coordinates:
            x,y = coordinate.split()
            geojson += f"""[{x}, {y}],"""
        geojson = geojson[:-1]
        geojson += """]]}},"""

    
        inside = False
        while(inside is not True):
                
            #Pick a starting point within the sector for the center of the first ship
            random_start_point = f"""SELECT ST_AsText(ST_GeneratePoints('{section}'::geometry, 1));"""
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
                        bearing = 90 if 'W' in sector else 270

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
            in_bounds = f"""SELECT ST_WITHIN(ST_GEOMFROMTEXT('{all_boats}'), ST_GEOMFROMTEXT('{section}'));"""
            cur.execute(in_bounds)
            inside = cur.fetchall()[0][0]
            #print(inside)
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
        return ship_dicts

def start():
    return "Hello World"
    time.sleep(1)

def getLoc():
    # every route needs hash
    url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        responseData = r.json() 
        print(responseData)

def posFleet():
    # every route needs hash
    try:
        url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            responseData = r.json() 
            print(responseData)
    except:
        return ""

def show_fleet_generation():
    output = []
    if(bbox != {}):
        for ship in generate_Fleet():
            output.append(json.dumps(ship, indent=4))
    return output


def shipSpeed():
    # # every route needs hash
    # url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

    # r = requests.get(url)
    # if r.status_code == requests.codes.ok:
    #     responseData = r.json() 
    #     print(responseData)
    with DatabaseCursor("config.json") as cur:
        #Make the bounding box and store it as a polygon
        query = f"""SELECT ship_id, speed FROM public.ship_state ORDER BY ship_id;"""

        cur.execute(query)
        result = cur.fetchall()
    display = "Speed of ships:\n"
    ships=[]

    for id, speed in result:
        display += "Ship "+ str(int(id))+" : Speed = "+str(int(speed))+'\n'
    
    return display
def turnShips():
    # # every route needs hash
    # url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

    # r = requests.get(url)
    # if r.status_code == requests.codes.ok:
    #     responseData = r.json() 
    #     print(responseData)
    global change
    with DatabaseCursor("config.json") as cur:
        ships = f"""SELECT ship_id, bearing FROM ship_state;"""
        cur.execute(ships)
        ships = cur.fetchall()
        print("These are the ships in your fleet:")
        for ship_id, bearing in ships:
            print("Ship_ID:", ship_id, '    Bearing:', bearing)

        print("Please Select Which Ships to turn seperated by spaces:\n")
        ships_select = input()
        ships_select = [int(x) for x in ships_select.split()]
        print("""Please Specify the how many degrees to rotate for each ship seperated by a space
        or give one bearing to change for all ships. Note if you wish to have ships change different bearings then all
        bearing must be given individually""")
        bearing_select = input()

        if(len(bearing_select.split()) == 1):
            bearing_select = [float(bearing_select) for x in ships_select]
        else:
            bearing_select = [float(x) for x in bearing_select.split()]

        for i in range(len(ships_select)):
            turn_ship = f"""SELECT ST_Rotate(
                ss.geom, RADIANS(-({bearing_select[i]} + ss.bearing)
                )) FROM public.ship_state as ss WHERE ship_id = {ships_select[i]};"""
            cur.execute(turn_ship)
            new_poly = cur.fetchall()[0][0]

            #Update ship_state based on ship's turn and new speed
            update_ship = f"""UPDATE ship_state SET bearing = (bearing + {bearing_select[i]})::int % 360, geom = '{new_poly}' WHERE ship_id = {ships_select[i]};"""
            cur.execute(update_ship)

        os.system('cls')
        ships = f"""SELECT ship_id, bearing FROM ship_state ORDER BY ship_id;"""
        cur.execute(ships)
        ships = cur.fetchall()
        print("Here is your updated Fleet:")
        for ship_id, bearing in ships:
            print("Ship_ID:", ship_id, '    Bearing:', bearing)

        
        url = f"https://battleshipgame.fun:8080/turn_ship/?hash={credentials['hash']}"

        payload = json.dumps({ 
            "fleet_id": 15,    
            "ship_id": ships_select,
            "bearing": bearing_select
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        input("Press Any Key to Continue:")
        change = True
        return



def showGuns():
    # # every route needs hash
    # url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

    # r = requests.get(url)
    # if r.status_code == requests.codes.ok:
    #     responseData = r.json() 
    #     print(responseData)
    global change
    with DatabaseCursor("config.json") as cur:
        ships = f"""SELECT ship_id::int FROM ship_state;"""
        cur.execute(ships)
        ships = cur.fetchall()
        print("These are the ships in your fleet:")
        for ship_id in ships:
            print("Ship_ID:", ship_id[0])

        print("Please Select Which Ships to View the Guns Of seperated by spaces:\n")
        ships_select = input()
        ships_select = [int(x) for x in ships_select.split()]
        
        os.system('cls')
        for ship in ships_select:
            guns = f"""SELECT gun_state.gun_id::int, type, ammo::int FROM gun_state, ships_guns where gun_state.ship_id = {ship}
            AND gun_state.gun_id = ships_guns.gun_id AND gun_state.ship_id = ships_guns.ship_id;"""
            cur.execute(guns)
            guns = cur.fetchall()
            print("SHIP_ID:", ship)
            for gun in guns:
                print("\n\n\tGUN_ID:", gun[0], "\tTYPE:", gun[1], "\tAMMO:", gun[2])
            print("-----------------------------------------------------------------------------")
       

        input("Press Any Key to Continue:")
        change = True
        return


def showShips():
    # # every route needs hash
    # url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

    # r = requests.get(url)
    # if r.status_code == requests.codes.ok:
    #     responseData = r.json() 
    #     print(responseData)
    global change
    with DatabaseCursor("config.json") as cur:
        ships = f"""SELECT ship_id::int, bearing::int, speed::int, location FROM ship_state;"""
        cur.execute(ships)
        ships = cur.fetchall()
        print("These are the ships in your fleet:")
        for ship_id, bearing, speed, loc in ships:
            print("Ship_ID:", ship_id, "\n\tBearing:", bearing, "   Speed:", speed, "     Location:", loc)
        
        input("Press Any Key to Continue:")
        change = True
        return
                



def fireGuns():
    # every route needs hash
    url = f"https://battleshipgame.fun/battleLocation/?hash={credentials['hash']}&fleet_id=kraken"

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        responseData = r.json() 
        print(responseData)

def game_bounds(version = "string"):
    global bbox
    global sector
    if(bbox == {}):
        bounds = get_GameBounds()
        bbox = bounds[0]
        sector = bounds[1]

    if(version == "string"):
        return [f"Game Bounds:\n  {bbox}", f"Sector:\n  {sector}\n"]
    else:
        return {"bbox" : {bbox}, "sector" : {sector}}


    
def main():
    global game_id
    global bbox
    global change
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)

    menu = ConsoleMenu("!!! TEAM KRAKEN !!!", 
    "Please choose one of the menu options...", formatter=menu_format, exit_option_text="EXIT")

    # A FunctionItem runs a Python function when selected
    #function_posfleet = FunctionItem("POSITION FLEET",posFleet)
    #function_shipspeed = FunctionItem("SHIPS SPEED",shipSpeed)

    # Using Sub menu to display messages for choosing a game
    selection_menu5 = ConsoleMenu(title="\tFleet Has Been Positioned:\t\t", formatter=menu_format)
    positionFleet_submenu = SubmenuItem("POSITION FLEET", selection_menu5, menu)

    subselection_menu5 = SelectionMenu(show_fleet_generation(), title= "\tKraken's Fleet:\t\t")
    viewwFleet_submenu = SubmenuItem("Show All Boats In Fleet", subselection_menu5, selection_menu5)
    selection_menu5.append_item(viewwFleet_submenu)

    # Using Sub menu to display messages
    selection_menu = SelectionMenu(["   LETS GET STARTED !!!        "])
    start_submenu = SubmenuItem("START", selection_menu, menu)

    selection_menu2 = SelectionMenu([shipSpeed()], "\tSHIPS SPEED\t\t")
    speed_submenu = SubmenuItem("SHIPS SPEED", selection_menu2, menu)
    
    # Using Sub menu to display messages for choosing a game
    selection_menu3 = SelectionMenu(Game_Choices(), title= "\tSELECT Which Game to Play:\t\t")
    games_submenu = SubmenuItem("GET CURRENT GAMES", selection_menu3, menu)

    # Using Sub menu to display messages for choosing a game
    selection_menu4 = ConsoleMenu(title="Fleet Has Been Generated:\t\t", formatter=menu_format)
    generateFleet_submenu = SubmenuItem("GENERATE FLEET", selection_menu4, menu)

    subselection_menu4 = SelectionMenu(show_fleet_generation(), title= "\tKraken's Fleet:\t\t")
    viewFleet_submenu = SubmenuItem("Show All Boats In Fleet", subselection_menu4, selection_menu4)
    selection_menu4.append_item(viewFleet_submenu)
  
    # Using Sub menu to display messages for choosing a game
    selection_menu6 = SelectionMenu(game_bounds(), title= "\tHere are the Game Bounds:\t\t")
    Location_submenu = SubmenuItem("GET BATTLE LOCATION", selection_menu6, menu)

    
    function_turnships = FunctionItem("TURN SHIPS",turnShips)
    function_showguns = FunctionItem("SHOW GUNS",showGuns)
    function_showships = FunctionItem("SHOW SHIPS",showShips)
    
    # adding items to the menu
    menu.append_item(start_submenu)
    menu.append_item(speed_submenu)
    menu.append_item(generateFleet_submenu)
    menu.append_item(games_submenu)
    menu.append_item(Location_submenu)
    menu.append_item(positionFleet_submenu)
    menu.append_item(function_turnships)
    menu.append_item(function_showguns)
    menu.append_item(function_showships)
    menu.exit_option_text = "EXIT"

    menu.start()
    while(menu.is_alive()):

        if(menu.current_item == games_submenu):
            # print(menu.current_option)
            # print('===')
            # print(menu.selected_option)
            selection_menu3.show()
            chosen_game = games_submenu.get_return()
            game_id = pick_Game(chosen_game) if chosen_game is not None else -1
            bbox = {}
            menu.remove_item(Location_submenu)

            #everything gets updated so I have to reload it all
            selection_menu2 = SelectionMenu([shipSpeed()], "\tSHIPS SPEED\t\t")
            speed_submenu = SubmenuItem("SHIPS SPEED", selection_menu2, menu)

            selection_menu6 = SelectionMenu(game_bounds(), title= "\tHere are the Game Bounds:\t\t")
            Location_submenu = SubmenuItem("GET BATTLE LOCATION", selection_menu6, menu)

            subselection_menu4 = SelectionMenu(show_fleet_generation(), title= "\tKraken's Fleet:\t\t")
            viewFleet_submenu = SubmenuItem("Show All Boats In Fleet", subselection_menu4, selection_menu4)

            subselection_menu5 = SelectionMenu(show_fleet_generation(), title= "\tKraken's Fleet:\t\t")
            viewwFleet_submenu = SubmenuItem("Show All Boats In Fleet", subselection_menu5, selection_menu5)

            print('Game Chosen: Press Enter to Return')          
            if(game_id != -1):
                change = True
            menu.current_option = 0 
            #print(game_id)


        # if(menu.current_item == function_turnships):
        #     if(change == True):
        #         menu.current_option = 0

        #         #print(game_id)

        #Menu hates dynamic changes to it but we are too far in so we have to compromise with it
        if(change == True):
            # #everything gets updated so I have to reload it all
            # selection_menu2 = SelectionMenu([shipSpeed()], "\t\tSHIPS SPEED\t\t")
            # speed_submenu = SubmenuItem("SHIPS SPEED", selection_menu2, menu)

            # selection_menu6 = SelectionMenu(game_bounds(), title= "\tHere are the Game Bounds:\t\t")
            # Location_submenu = SubmenuItem("GET BATTLE LOCATION", selection_menu6, menu)

            # subselection_menu4 = SelectionMenu(show_fleet_generation(), title= "\t\Kraken's Fleet:\t\t")
            # viewFleet_submenu = SubmenuItem("Show All Boats In Fleet", subselection_menu4, selection_menu4)

            # subselection_menu5 = SelectionMenu(show_fleet_generation(), title= "\t\Kraken's Fleet:\t\t")
            # viewwFleet_submenu = SubmenuItem("Show All Boats In Fleet", subselection_menu5, selection_menu5)
            
            menu.items = []
            menu.append_item(start_submenu)
            menu.append_item(speed_submenu)
            menu.append_item(generateFleet_submenu)
            menu.append_item(games_submenu)
            menu.append_item(Location_submenu)
            menu.append_item(positionFleet_submenu)
            menu.append_item(function_turnships)
            menu.append_item(function_showguns)
            menu.append_item(function_showships)

            selection_menu4.items = []
            selection_menu5.items = []
            selection_menu4.append_item(viewFleet_submenu)
            selection_menu5.append_item(viewwFleet_submenu)
            menu.add_exit()
            change = False

        # # if(menu.current_item == Location_submenu):
        # #     try:
                
        # #         selection_menu5.exit()
        # #         #Location_submenu.get_return()
        # #         menu.current_option = 0
        # #         #selection_menu5.exit()
        # #         print("Press Enter to Return to Previous Screen:")
        # #         print(game_bounds())


        #     except Exception as e:
        #         print(e)



    menu.join()

if __name__ == '__main__':
    main()
    #generate_Fleet()

    geojson = geojson[:-1] + "]}"
    with open("shipLocations.json", 'w') as f:
        f.write(geojson)
        
    outputFile = {'fleet_id' : "kraken", "ship_status" : ship_dicts}
    with open("final_output.json", 'w') as f:
        f.write(json.dumps(outputFile, indent=4))