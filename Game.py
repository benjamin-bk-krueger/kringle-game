import os
import json
from Object import Object
from Room import Room
from Objective import Objective

cont = 1        # set to 0 when the program should quit
location = 1    # the starting room always has ID 1, changes later in the game
rows = 24       # default terminal heigth
columns = 80    # default terminal width, necessary to render ansii images

rooms = dict()          # contains all available rooms
objectives = dict()     # contains all available objectives

# ANSII images have been created with the help of https://manytools.org/hacker-tools/convert-image-to-ansi-art/
# size formats: 80, 160 characters

# all the actions the player can perform
def arrive():
    print ("You are arriving at a strange location.")
    print ("You are feeling a little dizzy.")

def lost():
    print("You're feeling lost somehow. You could *cry* for help to see what happens.")

def help():
    print("A magical voice whispers into your ear. Following commands are available:")
    print("cry, exit, help, inspect, medidate, scout, talk, quit")

def inspect():
    print("You are inspecting the place and looking around...")
    display_image(rooms.get(location).image)
    print(rooms.get(location).description)

    for id in objectives:
        if (objectives[id].location == location):
            print("In this room you can see " + objectives[id].name + ", " + objectives[id].description + ".")

def meditate():
    print("A quest to save Santa has brought you to this place.")
    print("You think about all those creatures here could help you.")

def scout():
    print("You have arrived at " + rooms.get(location).name)

def talk():
    print("You decide to talk to ...")
    for id in objectives:
        if (objectives[id].location == location):
            print(str(id) + ": " + objectives[id].name)
    talk = input("--> ")
    for id in objectives:
        if (objectives[id].location == location):
            if (str(id) == talk):
                print("You are talking to " + objectives[id].name)
                display_image(objectives[id].image)
            else:
                print("... no one here in the room.")

# helper functions
def display_image(image_name):
    if (columns < 80):
        print("...but your view space is too small to see all the details.")
    elif (columns >= 80 and columns < 160):
        img = open("res/" + image_name + "_s.ans", "r")
        print(img.read())
    else:
        img = open("res/" + image_name + "_m.ans", "r")
        print(img.read())

def load_data():
    f = open("data.json")
    data = json.load(f)
    for i in data["rooms"]:
        room = Room()
        room.name = i["name"]
        room.description = i["description"]
        room.image = i["image"]
        rooms.update({i["id"]: room})
    for i in data["objectives"]:
        objective = Objective()
        objective.name = i["name"]
        objective.description = i["description"]
        objective.image = i["image"]
        objective.location = i["location"]
        objectives.update({i["id"]: objective})
    f.close()

def query_user():
    global cont
    cmd = input("> ")
    if (cmd == "help"):
        help()
    elif (cmd == "cry"):
        help()
    elif (cmd == "exit"):
        cont = 0
    elif (cmd == "inspect"):
        inspect()
    elif (cmd == "medidate"):
        meditate()
    elif (cmd == "scout"):
        scout()
    elif (cmd == "talk"):
        talk()
    elif (cmd == "quit"):
        cont = 0
    else:
        lost()

# open the JSON data file and build all object dictionnaries
load_data()

# start the game until the player decides to quit
arrive()
meditate()

while (cont == 1):
    s_rows, s_columns = os.popen('stty size', 'r').read().split()
    rows = int(s_rows)
    columns = int(s_columns)
    query_user()