import json
from Room import Room

location = 1 # the starting room always has ID 1, changes later in the game

# all the actions the player can do
def lost():
    print("You're feeling a little lost.")
    print("You could *cry* for help.")

def help():
    print("Following commands are available:")
    print("cry, help, inspect, look, quit")

def inspect():
    print("You are inspecting the place, it looks like")
    print("")
    print(rooms.get(location).image)

def look():
    print("You have arrived at " + rooms.get(location).name)

# open the JSON data file and build all object dictionnaries
rooms = dict()

f = open("data.json")
data = json.load(f)

for i in data["rooms"]:
    room = Room()
    room.name = i["name"]
    # images have been created here: https://manytools.org/hacker-tools/convert-image-to-ansi-art/
    # size: 160 characters
    img = open(i["image"], "r")
    room.image = img.read()
    rooms.update({int(i["id"]): room})

f.close()

# start the game until the player decides to quit
while True:
    cmd = input("> ")
    if (cmd == "help"):
        help()
    elif (cmd == "cry"):
        help()
    elif (cmd == "look"):
        look()
    elif (cmd == "inspect"):
        inspect()
    elif (cmd == "quit"):
        break
    else:
        lost()
