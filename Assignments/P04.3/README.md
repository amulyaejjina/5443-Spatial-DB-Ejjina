## Project 4.3
#### 12/6/2022
## Menu & Comms For Battleship
# 

#### Team Members:
##### Allyson Warren, Amulya Ejjina, Mihriban Guneydas
#
#### Description: 
This project is for a battleship game using FASTAPI and PostgreSQL. The goal of this project is to determine
how to move and utilize a given number of ships assigned to one's fleet. The actions dictated by how we choose to
move our fleet are done through the utilization of a console menu using the open source code from console-menu. 
For this project, there are 9 options that can be performed from our menu:

<img src="images\Capture.PNG" width="500" />

- Start
  - Begin playing battleship and start accessing the api
- Ships Speed
  - View the speeds of all ships within our fleet at once
- Generate Fleet
  - Make our fleet and position it onto the game board within our given section
- Get Current Games
  - See what games are available to play from the api and choose one to play
- Get Battle Location
  - To be called after Get Current Games: gets the bounding box of the game's playing field and what section we start at
- Position Fleet
  - Position the Fleet within our section. Similar to Generate Fleet but does not reload the database.
- Turn Ships
  - Turn a selection of ships by a given number of degrees. Updates the geometry and bearing of the ship in the database
- Show Guns
  - Display the available guns and ammo within a selected number of ships
- Show Ships
  - Display the information of all ships within our fleet at a given time
- Exit
  - Default option to close the program and leave the menu

The menu is to eventually also incorporate turing a gun, firing a gun, and moving ships; however,
due to time constraints, this is to be implemented at a later date. The focus of the menu for now
is being able to properly communicate with the battleship api and utilize the information given to us
to be able to play a current active game and position a given fleet obtained through the api within
a given section in order to begin playing.

Along with the menu, we also utilize a communication terminal that allows us to communicate
with other teams playing battleship as well. This is done using RabbitMQ where each team
is given a user id and password. For the communication aspect, there are two ways to utilize it.
The first is to directly send a message to a team using their team name(id). Giving a command like:
"kraken~ hello" will send a direct message to the team kraken and no other team will receive the message. 
On the other side, we are also able to send a message to everyone actively listening on the battleship api.
This is done by sending "broadcast~ hello" such that all teams receive a message saying hello. The intention
of the communication is to allow teams to coordinate or strategize based on the input of other teams.


For this project, you must install console-menu to access the menu interface.
To do this, use:
- pip install console-menu
- include the consolemenu folder found in our project within your code.

After installing and implementing the necessary files for the console menu, run the following for each
of the items for this project:
- Menu:                        python menu.py
- Sending Messages:            python sender.py
- Listening for Messages:      python listener.py