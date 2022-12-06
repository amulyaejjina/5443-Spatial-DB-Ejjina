## Project 4.2
#### 11/27/2022
## Database Creation for Battleship
# 

#### Team Members:
##### Allyson Warren, Amulya Ejjina, Mihriban Guneydas
#
#### Description: 
This code updates the progress from [P04.1](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1) and
includes the implementation of creating tables that will be needed for the battleship game. The tables that are implemented in for this
project are: 
|   #   | Table Name | Description |
| :---: | ----------- | ---------------------- |
|  01  | [cardinalDegrees](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/cardinalDegrees.sql) | Contains the degrees of each section in the game's bounds |
|  02  | [cartridge](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/cartridge.sql) | Contains the ammo cartridge of all gatlin guns and its information |
|  03  | [enemy_sightings](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/enemy_sightings.sql) | Contains the info gathered about any teams we come across such as the sighting direction and accuracy of sight |
|  04  | [gun_state](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/gun_state.sql) | Contains the info of a specific gun. Each gun is identified by its ship_id and it's own unique id within the ship. It keeps track of ammo amount and bearing of a gun |
|  05  | [gun](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/gun.sql) | Contains the info of all the types of guns. Keeps track of a general gun type's info such as mm and ammo type |
|  06  | [projectile](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/projectile.sql) | Contains the info about projectile ammo. This ammo is for mounted guns. It contains its length and mass |
|  07  | [ship_state](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.2/SQL%t20able%20and%20queries/tables/ship_state.sql) | Contains the info of a specific ship. Each ship is identified by its unique ship_id. It keeps track of the ships location, speed, and bearing at a given time |
|  08  | [ship](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/ship.sql) | Contains the info of a the different types of ships. It holds information such as type of ship and its classification |
|  09  | [ships_guns](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/ships_guns.sql) | Contains the info of a particular ship's guns. Each gun is identified by a ship's id and its own unique id within the ship. It hold information such as type of gun and its position on the ship |
|  10  | [torpedo_state](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/torpedo_state.sql) | Contains the info of a particular ship's torpedo. Each torpedo is identified by a ship's id and its own unique id within the ship. It hold information such as location on the ship and what type it is |
|  11  | [torpedo](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/tables/torpedo.sql) | Contains the info of a general torpedo. Holds information such as it mass, diameter, warhead size, etc.|


Queries were made using these tables to test accessing data within postgresql and utilizing postgis functions to obtain information.
The code for the queries that were considered can be found here [queries](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/queries/queries.py) and the results obtained from each query is here: [results](https://github.com/apwarren/5443-Spatial-DB-Warren/blob/main/Assignments/P04.2/SQL%20tables%20and%20queries/queries/queries.json). Queries considered were:
- rotating the entire fleet a certain number of degrees
- rotating a single ship a certan number of degrees
- rotating a specific gun on a particular ship and changing its elevation given the type of gun it is
- Firing a projectile from a gun and getting its path from the ship to a given distance after so many seconds

Each query is done using postgis functions and only accessing our created tables within our database. This is the initial
starting point of incorporating our ships' actions to consider how to move and attack other ships in the game. 
