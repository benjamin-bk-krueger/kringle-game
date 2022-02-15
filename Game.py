import os
import json
from Object import Object
from Room import Room
from Objective import Objective

location = 1 # the starting room always has ID 1, changes later in the game
rows = 24 # default terminal heigth
columns = 80 # default terminal width, necessary to render ansii images

rooms = dict()
objectives = dict()

# all the actions the player can do
def lost():
    print("You're feeling lost somehow.")
    print("You could *cry* for help.")

def help():
    print("A magical voice whispers into your ear.")
    print("Following commands are available:")
    print("cry, exit, help, inspect, look, quit, remember")

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

    for id in objectives:
        print(objectives[id].location)
        if (objectives[id].location == location):
            print("In this room you can see " + objectives[id].name + " which is " + objectives[id].description)


def look():
    print("You have arrived at " + rooms.get(location).name)

def remember():
    print("A quest to save Santa has sent you here.")
    print("You think about all those creatures here could help you.")

# open the JSON data file and build all object dictionnaries
f = open("data.json")
data = json.load(f)

for i in data["rooms"]:
    room = Room()
    room.name = i["name"]
    room.description = i["description"]
    room.image = i["image"]
    rooms.update({int(i["id"]): room})

for i in data["objectives"]:
    objective = Objective()
    objective.name = i["name"]
    objective.description = i["description"]
    objective.image = i["image"]
    objective.location = i["location"]
    objectives.update({int(i["id"]): objective})

f.close()

# start the game until the player decides to quit
print ("You are arriving at a strange location.")
print ("You are feeling a little dizzy.")
print ("")
remember()

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
    elif (cmd == "remember"):
        remember()
    else:
        lost()
