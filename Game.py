import os       # necessary to access terminal size
import json     # necessary to read json-based data file
import readline # necessary to be able to auto-complete user

from Room import Room
from Objective import Objective
from Junction import Junction

cont = 1                # the program will run until this value is set to 0
location = 1            # the starting room always has ID 1, changes later in the game by walking around
rows = 24               # default terminal heigth
columns = 80            # default terminal width, necessary to render ansii images

rooms = dict()          # contains all available rooms
objectives = dict()     # contains all available objectives
junctions = dict()      # contains all junctions between the rooms

settings = dict()       # holds all game settings

volcab = []             # contains autocomplete values
default_actions = ['help','cry','beam','exit','inspect','look','meditate','scrutinize','talk','phone','quit','walk'] # default actions

# ANSII images have been created with the help of https://manytools.org/hacker-tools/convert-image-to-ansi-art/
# size formats: 80, 160 characters (s, m format)

# all the actions the player can perform
# only triggered once automatically when the player arrives (starts the program) - no command assigned
def arrive():
    display_image(settings["logo"])
    print("")
    print("You are arriving at a strange and unknown location.")
    print("You are feeling a little dizzy.")
    rooms.get(location).visited = True

# get some about information - "scrutinize" command assigned
def scrutinize():
    print("A magical voice whispers into your ear:")
    print("\"This game has been created by Ben Krueger\"")
    print("You wonder what this may mean? A game? Strange thought")

# triggered automatically when the player enters a wrong command - no command assigned
def lost():
    print("You are feeling lost somehow. You could cry for help to see what happens.")

# shows all available commands - "help" command assigned
def help():
    print("A magical voice whispers into your ear: \"Following commands are available\"")
    print(default_actions)
    print("Then it whispers: \"TAB is your friend\"")
    print("You wonder what this TAB may be? A creature? A scroll?")

# have a detailed look what kind of objects a room contains - "inspect" command assigned
def inspect():
    print("You are inspecting the place and looking for further objects you can interact with...")

    for id in objectives:
        if (objectives[id].location == location):
            print("In this room you can see " + objectives[id].name + ", " + objectives[id].description + ".")
            print("    " + objectives[id].name + " seems to know something about a main objective.")
            if (objectives[id].visited):
                print("    " + "You already have talked to " + objectives[id].name + " before.")
            else:
                print("    " + "You have not talked to " + objectives[id].name + " yet.")
    
    for id in junctions:
        if (junctions[id].location == location):
            print(junctions[id].description + " you can see a junction to " + rooms.get(junctions[id].destination).name)
            if (rooms.get(junctions[id].destination).visited):
                print ("    " + "You have visited that location already.")
            else:
                print ("    " + "You have not seen that location yet.")

# think about the main quest in the game, triggered automatically when the player arrives - "meditate" command assigned
def meditate():
    print("A quest to save Santa has brought you to this place.")
    print("You think about all those creatures here could help you.")

# have a quick look at this place - "look" command assigned
def look():
    print("You are currently at " + rooms.get(location).name + " and admiring what your eyes can see...")
    display_image(rooms.get(location).image)
    print(rooms.get(location).description)

# phone other creatures you already have discovered - "phone" command assigned
def phone():
    # necessary for creature name auto-completion
    global volcab
    new_volcab = []

    print("You put your hand into your right pocket and grab a magical device.")
    print("It has a display where you can see the names of all the creatures you had contact with.")
    print("You guess you can open some channel to a creature by tapping its name.")

    # assign all visited creatures to the auto-completion list
    counter = 0
    for id in objectives:
        if (objectives[id].visited):
            counter = counter + 1
            new_volcab.append(objectives[id].name)
            print("  Entry: " + objectives[id].name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        talk = input("I want to talk to > ")
        for id in objectives:
            if (objectives[id].visited):
                if (objectives[id].name == talk):
                    print("You are talking to " + objectives[id].name)
                    display_image(objectives[id].image)
                    break
                else:
                    print("You decide you don't want to talk right now.")
                    break
    else:
        print("After a moment you realize you have not met anyone yet.")
    set_default_complete()
    
# talk to other creatures - "talk" command assigned
def talk():
    # necessary for creature name auto-completion
    global volcab
    new_volcab = []

    # assign all creatures in this room to the auto-completion list
    counter = 0
    for id in objectives:
        if (objectives[id].location == location):
            counter = counter + 1
            new_volcab.append(objectives[id].name)
            print("  Entry: " + objectives[id].name)

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
                    break
                else:
                    print("You decide you don't want to talk right now.")
                    break
    else:
        print("After a moment you realize no one is in this room.")
    set_default_complete()

# beam to places you already have discovered - "beam" command assigned
def beam():
    # necessary for room name auto-completion and new room selection
    global volcab
    global location
    new_volcab = []

    print("You put your hand into your left pocket and grab a magical device.")
    print("It has a display where you can see the names of all the places you have visited.")
    print("You guess you can travel there by tapping its name.")

    # assign all visited rooms to the auto-completion list
    counter = 0
    new_location = 1
    for id in rooms:
        if (rooms[id].visited):
            counter = counter + 1
            new_volcab.append(rooms[id].name)
            print("  Entry: " + rooms[id].name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        walk = input("I want to go to > ")
        for id in rooms:
            if (rooms[id].visited):
                if (rooms[id].name == walk):
                    print("You are going to " + rooms[id].name)
                    new_location = id
                    break
                else:
                    new_location = location
                    print("You decide to stay where you currently are.")
                    break
    else:
        new_location = location
        print("After a moment you realize you have not been anywhere yet.")
    location = new_location
    set_default_complete()

# walk to other places - "walk" command assigned
def walk():
    # necessary for room name auto-completion and new room selection
    global volcab
    global location
    new_volcab = []

    # assign all connected rooms to the auto-completion list
    counter = 0
    new_location = 1
    for id in junctions:
        if (junctions[id].location == location):
            counter = counter + 1
            new_volcab.append(rooms.get(junctions[id].destination).name)
            print("  Entry: " + rooms.get(junctions[id].destination).name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print ("")
        walk = input("I want to go to > ")
        for id in junctions:
            if (junctions[id].location == location):
                if (rooms.get(junctions[id].destination).name == walk):
                    print("You are going to " + rooms.get(junctions[id].destination).name)
                    new_location = junctions[id].destination
                    rooms.get(junctions[id].destination).visited = True
                    break
                else:
                    new_location = location
                    print("You decide to stay where you currently are.")
                    break
    else:
        new_location = location
        "After a moment you realize there is no way out of this room."
    location = new_location
    set_default_complete()

# helper functions, cannot be triggered by the player directly
# resets the auto-completion to the default actions list
def set_default_complete():
    global volcab
    volcab = default_actions

# sets the auto-completion list to a custom one (necessary for creature and room auto-completion)
def set_custom_complete(list):
    global volcab
    volcab = list

# auto-completion with Python readline, requires readline
def complete(text,state):
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

# displays a colored ANSII image, depending on the terminal size, requires os
def display_image(image_name):
    if (columns < 80):
        print("...but your view space is too small to see all the details.")
    elif (columns >= 80 and columns < 160):
        img = open("images/" + image_name + "_s.ans", "r")
        print(img.read())
    else:
        img = open("images/" + image_name + "_m.ans", "r")
        print(img.read())

# parses the JSON based configuration file and creature objects from that configuration, requires json
def load_data():
    global settings

    f = open("data.json")
    data = json.load(f)
    settings = data["settings"]
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
    for i in data["junctions"]:
        junction = Junction()
        junction.destination = i["destination"]
        junction.description = i["description"]
        junction.location = i["location"]
        junctions.update({i["id"]: junction})
    f.close()

# queries the user to enter a command and triggers the matching function
def query_user():
    global cont
    print("")
    cmd = input("I want to > ")
    if (cmd == "help"):
        help()
    elif (cmd == "cry"):
        help()
    elif (cmd == "beam"):
        beam()
    elif (cmd == "exit"):
        cont = 0
    elif (cmd == "inspect"):
        inspect()
    elif (cmd == "look"):
        look()
    elif (cmd == "meditate"):
        meditate()
    elif (cmd == "scrutinize"):
        scrutinize()
    elif (cmd == "talk"):
        talk()
    elif (cmd == "phone"):
        phone()
    elif (cmd == "quit"):
        cont = 0
    elif (cmd == "walk"):
        walk()
    else:
        lost()

# start of the main program
# -------------------------
# sets default for command auto-completion
set_default_complete()
#readline.parse_and_bind("tab: complete") # Linux
readline.parse_and_bind ("bind ^I rl_complete") # Mac
readline.set_completer(complete)

# get terminal size
s_rows, s_columns = os.popen('stty size', 'r').read().split()
rows = int(s_rows)
columns = int(s_columns)

# open the JSON data file and build all object dictionnaries
load_data()

# start the game until the player decides to quit
arrive()
print("")
meditate()

while (cont == 1):
    # get terminal size - maybe the user has resized the window
    s_rows, s_columns = os.popen('stty size', 'r').read().split()
    rows = int(s_rows)
    columns = int(s_columns)
    query_user()