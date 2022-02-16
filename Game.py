import os       # necessary to access terminal size
import json     # necessary to read json-based data file
import readline # necessary to be able to auto-complete user

from Object import Object
from Room import Room
from Objective import Objective

cont = 1        # set to 0 when the program should quit
location = 1    # the starting room always has ID 1, changes later in the game
rows = 24       # default terminal heigth
columns = 80    # default terminal width, necessary to render ansii images

rooms = dict()          # contains all available rooms
objectives = dict()     # contains all available objectives

volcab = []             # contains autocomplete values

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
    print("Then it whispers:")
    print("TAB is your friend")

def inspect():
    print("You are inspecting the place and looking around...")
    display_image(rooms.get(location).image)
    print(rooms.get(location).description)

    for id in objectives:
        if (objectives[id].location == location):
            print("In this room you can see " + objectives[id].name + ", " + objectives[id].description + ".")
            print("    " + objectives[id].name + " seems to know something about a main objective.")
            if (objectives[id].visited):
                print("    " + "You already have talked to " + objectives[id].name + " before.")
            else:
                print("    " + "You have not talked to " + objectives[id].name + " yet.")

def meditate():
    print("A quest to save Santa has brought you to this place.")
    print("You think about all those creatures here could help you.")

def scout():
    print("You have arrived at " + rooms.get(location).name)

def talk():
    global volcab
    new_volcab = []
    counter = 0
    for id in objectives:
        if (objectives[id].location == location):
            counter = counter + 1
            new_volcab.append(objectives[id].name)
    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        talk = input("I want to talk to > ")
        for id in objectives:
            if (objectives[id].location == location):
                if (objectives[id].name == talk):
                    print("You are talking to " + objectives[id].name)
                    display_image(objectives[id].image)
                    objectives[id].visited = True
                else:
                    print("You decide you don't want to talk right now.")
    else:
        "After a moment you realize no one is in this room."
    set_default_complete()

# helper functions
def set_default_complete():
    global volcab
    volcab = ['help','cry','exit','inspect','meditate','scout','talk','quit']

def set_custom_complete(list):
    global volcab
    volcab = list

def complete(text,state):
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

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
    print("")
    cmd = input("I want to > ")
    if (cmd == "help"):
        help()
    elif (cmd == "cry"):
        help()
    elif (cmd == "exit"):
        cont = 0
    elif (cmd == "inspect"):
        inspect()
    elif (cmd == "meditate"):
        meditate()
    elif (cmd == "scout"):
        scout()
    elif (cmd == "talk"):
        talk()
    elif (cmd == "quit"):
        cont = 0
    else:
        lost()

set_default_complete()
#readline.parse_and_bind("tab: complete") # Linux
readline.parse_and_bind ("bind ^I rl_complete") # Mac
readline.set_completer(complete)

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