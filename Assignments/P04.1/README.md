## Project 4.1
#### 11/22/2022
## Ship Generation for Battleship
# 

#### Team Members:
##### Allyson Warren, Amulya Ejjina, Mihriban Guneydas
#
#### Description: 
This code takes the upper left and bottom right coordinates of a bounding box representing the given field
of a game of battleship. This field is divided into sectors based on different degrees and there are 16 total 
sectors that can be assigned to any given team. Each team is assigned a random sector. Once given our sector, this
code gets the bounds of the sector and then uses ST_Split to cut it out and separate it from the overall field's bounding
box. Once the sector is retrieved, a random start point is then generated within the sector. This point
represents the center of our first battleship. Given a list of ships from [ships.json](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/ships.json), we generate each ship starting
from the top left corner. Each row gets a maximum of the square root of the total number of ships to ensure they are clustered
properly. Each ship is then spaced out 222m from bow to stern from each other and 111m from port to starboard. Each row is
also staggered to keep them clustered but relatively spaced out. After all ships are generated, each one's center point is stored along
with its bearing. The bearing of each ship faces away from the fields bounds. All final data generated is then dumped into [final_output.json](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/final_output.json) along with the name of the fleet.

#### <u> A simplified series of steps explained above: </u>
- Get the game field's bounding box and which sector we are assigned
- Seperate the sector from the bounding box and store it as a seperate polygon
- Generate a random starting point within the sector
- Generate all ships we are given with 222m spacing bow to stern and 111m spacing port to starboard
- Store the center of each ship
- Give each ship a bearing facing away from the game field's outer bounds
- Push all ship information and the name of our fleet to [final_output.json](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/final_output.json)

#### Visual of the sector seperate from the bounding box using geojson.io
<img src="https://user-images.githubusercontent.com/70217207/204109786-1ab6a067-88c5-43fb-a3a2-03ee18bec5fc.png" width="300" />

#### Close up visual of all ships generated within the sector using geojson.io
<img src="https://user-images.githubusercontent.com/70217207/204109807-344abae6-a6cf-4be0-b5ce-34de1cbbca96.png" width="300" />

|   #   | File Link | Description |
| :---: | ----------- | ---------------------- |
|  01  | [main.py](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/main.py) | main python file. Contains all code for generating ships in a given sector of the game's bounding box |
|  02  | [ships.json](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/ships.json) | json file containing all ships we have in the fleet |
|  03  | [cardinalDegrees.sql](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/cardinalDegrees.sql) | sql file containing the bounds for each sector and its degrees
|  04  | [shipLocations.json](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/shipLocations.json) | json file storing each ship's location as a geojson. This file is primarily for testing purposes
|  05  | [final_output.json](https://github.com/apwarren/5443-Spatial-DB-Warren/tree/master/Assignments/P04.1/final_output.json) | json file containing all information such as bearing and location of each ship
