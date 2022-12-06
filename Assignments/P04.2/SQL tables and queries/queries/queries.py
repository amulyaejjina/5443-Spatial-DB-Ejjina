import psycopg2
import json
import time

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

with DatabaseCursor("config.json") as cur:

    #Query 1: Turing a ship and setting its new postition in the table

    #Move all ships 60 degrees and update its polygon in the ship_state
    turn_fleet = f"""SELECT ss.ship_id::int, mod((ss.bearing + 60)::int, 360), ST_AsText(
        ST_Rotate(ss.geom, RADIANS((60 + ss.bearing) * 1)
        ))
         FROM public.ship_state as ss LIMIT 5;"""
    cur.execute(turn_fleet)
    new_poly = cur.fetchall()

    for i in range(len(new_poly)):
        head = ['ship_id', 'bearing', 'geometry']
        new_poly[i] = dict(zip(head, new_poly[i]))

    with open('queries.json', 'w') as f:
        f.write('// Query 1 Result:\n')
        f.write(json.dumps(new_poly, indent=4))

    #Update ship_state based on ship's turn
    # update = f"""UPDATE ship_state SET bearing = (60 + bearing)::int % 360, geom = '{new_poly}' WHERE ship_id = 1;"""
    # cur.execute(update)


    #Query2
    #Change the direction and speed of the seventh ship by 40 degrees and 25 m/s
    turn_ship = f"""SELECT ST_Rotate(ss.geom, RADIANS(40 + ss.bearing)) FROM public.ship_state as ss WHERE ship_id = 7;"""
    cur.execute(turn_ship)
    new_poly = cur.fetchall()[0][0]

    #Update ship_state based on ship's turn and new speed
    update = f"""UPDATE ship_state SET speed = 25, bearing = (bearing + 40)::int % 360,  geom = '{new_poly}' WHERE ship_id = 7;"""
    cur.execute(update)

    update = f"""SELECT ship_id::int, speed::int, bearing, ST_AsText(geom) FROM ship_state WHERE ship_id = 7;"""
    cur.execute(update)
    update = cur.fetchall()[0]

    head = ["ship_id", 'new_speed', 'bearing', 'new_rotation']
    file = dict(zip(head, update))
        
    with open('queries.json', 'a') as f:
            f.write("\n\n// Query 2 Result\n")
            f.write(json.dumps(file, indent=4))


    #Query3
    #Rotate the Mark13 gun in ship 2 by 10 degrees and elevate it by 5 degrees
    rotate_gun = f"""UPDATE gun_state
     SET bearing = (bearing + 10)::int % 360, elevation = (elevation + 5)::int % 45
     FROM ships_guns
     WHERE gun_state.ship_id = 2 and ships_guns.type = 'Mark13';"""
    cur.execute(rotate_gun)
    cur.execute("""SELECT gs.ship_id::int, gs.gun_id::int, type, bearing, elevation 
    FROM gun_state as gs, ships_guns as sg 
    WHERE gs.ship_id = sg.ship_id AND gs.gun_id = sg.gun_id
    AND sg.type = 'Mark13' AND sg.ship_id = 2""")
    head = ['ship_id', 'gun_id', 'type', 'bearing', 'elevation']
    info = cur.fetchall()[0]
    file = dict(zip(head, info))
       
    with open('queries.json', 'a') as f:
            f.write("\n\n// Query 3 Result\n")
            f.write(json.dumps(file, indent=4))


    #Query 4
    #Fire a Mark8 gun from ship 0. Get the path of the projectile after 10 seconds
    #Need to check if I'm doing this right
    rof = f"""SELECT rof::int FROM ship_state as ss, gun_state as gs, projectile as prj, gun as g, ships_guns as shg
    WHERE ss.ship_id = 0 AND g.name = shg.type AND g.name = 'Mark8' AND shg.type = 'Mark8'
    AND prj.name = g.ammotype LIMIT 1;
    """
    cur.execute(rof)
    rof = cur.fetchall()[0][0]

    center_point = f"""ST_MakePoint((ss.location->>'lon')::float, (ss.location->>'lat')::float)"""
    projected_point = f"""ST_Project({center_point}, prj.mm::int * 10, RADIANS(gs.bearing))"""
    fire_gun = f"""SELECT ST_AsText(
        ST_MakeLine(
            ST_SetSRID({center_point}, 4326),
             ST_SetSRID({projected_point}::geometry, 4326)
            ))
    FROM ship_state as ss, gun_state as gs, projectile as prj, gun as g, ships_guns as shg
    WHERE ss.ship_id = 0 AND g.name = shg.type AND g.name = 'Mark8' AND shg.type = 'Mark8'
    AND prj.name = g.ammotype LIMIT {rof};"""
    cur.execute(fire_gun)
    path = cur.fetchall()[0][0]
    info = f"""SELECT ship_id::int, gun_id::int, type from ships_guns WHERE ship_id = 0 AND type = 'Mark8' LIMIT 1;"""
    cur.execute(info)

    head = ['ship_id', 'gun_id', 'type', 'path']
    info = list(cur.fetchall()[0])
    info.append(path)
    file = dict(zip(head, info))
       
    with open('queries.json', 'a') as f:
            f.write("\n\n// Query 4 Result\n")
            f.write(json.dumps(file, indent=4))
    
    #Update ammo of the ship that fired. More than one round can be fired at once
    update = f"""UPDATE gun_state SET ammo = ammo - {rof} from ships_guns
    WHERE ships_guns.gun_id = gun_state.gun_id AND ships_guns.type = 'Mark8' AND gun_state.ship_id = 0;"""
    cur.execute(update)

