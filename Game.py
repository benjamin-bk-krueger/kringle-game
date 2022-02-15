import os
import json
from Room import Room

location = 1 # the starting room always has ID 1, changes later in the game
rows = 24
columns = 80

# all the actions the player can do
def lost():
    print("You're feeling lost somehow.")
    print("You could *cry* for help.")

def help():
    print("A magical voice whispers into your ear.")
    print("Following commands are available:")
    print("cry, exit, help, inspect, look, quit")

def inspect():
    print("You are inspecting the place, it looks like")
    # images have been created here: https://manytools.org/hacker-tools/convert-image-to-ansi-art/
    # size: 80 and 160 characters
    if (columns < 80):
        print("Your view space is too small to see all details")
    elif (columns >= 80 and columns < 160):
        img = open("res/" + rooms.get(location).image + "_s.ans", "r")
        print(img.read())
    else:
        img = open("res/" + rooms.get(location).image + "_m.ans", "r")
        print(img.read())
    print(rooms.get(location).description)

def look():
    print("You have arrived at " + rooms.get(location).name)

# open the JSON data file and build all object dictionnaries
rooms = dict()

f = open("data.json")
data = json.load(f)

for i in data["rooms"]:
    room = Room()
    room.name = i["name"]
    room.description = i["description"]
    room.image = i["image"]
    rooms.update({int(i["id"]): room})

f.close()

# start the game until the player decides to quit
print ("You are arriving at a strange location.")
print ("You are feeling a little dizzy.")
while True:
    s_rows, s_columns = os.popen('stty size', 'r').read().split()
    rows = int(s_rows)
    columns = int(s_columns)

    cmd = input("> ")
    if (cmd == "help"):
        help()
    elif (cmd == "cry"):
        help()
    elif (cmd == "exit"):
        break
    elif (cmd == "look"):
        look()
    elif (cmd == "inspect"):
        inspect()
    elif (cmd == "quit"):
        break
    else:
        lost()
