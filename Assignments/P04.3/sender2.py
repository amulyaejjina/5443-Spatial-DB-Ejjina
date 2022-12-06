"""
Example sender with some helper code to format and parse commands 
"""

from comms import CommsSender
import json


def help():
    print("=" * 60)
    print("Commands are formatted like the following examples: ")
    print('    stalin.fire ~ {"lon":2.345,"lat":10.1234,"angle":30.23,"kg":1200}')
    print("    broadcast ~ Stalin is going down!")
    print("The tildes (~) are used as an easy character to split on!")
    print("=" * 60)


def parseCommand(cmd):
    targetName = None
    msgAction = None

    cmd, data = cmd.split("~")
    cmd = cmd.strip()
    data = data.strip()
    if "broadcast" in cmd:
        msgAction = "broadcasting"
        targetName = "everyone"
    if "fire" in cmd:
        targetName, _ = cmd.split(".")
        msgAction = "firing"
        data = json.loads(data)  # turn it into json if you need to "access" it.

    return {"cmd": cmd, "data": data, "msgAction": msgAction, "targetName": targetName}


creds = {
     "id": 15,
     "name": "kraken",
     "regdate": 1669156402,
     "exchange": "battleship",
     "port": 5672,
     "host": "battleshipgame.fun",
     "password": "kX3aF8x5z0Sw",
     "hash": "32223921880817397656263709201856725525",
     "user" : "kraken"
 }

#team = creds["user"]
team = creds["name"]
commsSender = CommsSender(**creds)
txt = 1

while txt:
    txt = input("Enter ['command','quit','help']:")
    if txt == "help":
        help()
    elif txt == "quit":
        print("quitting...")
        break
    else:
        cmd = parseCommand(txt)
        print(f"{cmd['msgAction']} at/to {cmd['targetName']}")

        # turn the json back into a string to send it
        commsSender.sendCommand(cmd["cmd"], json.dumps(cmd["data"]))

commsSender.closeConnection()