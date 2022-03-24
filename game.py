import os               # necessary to access terminal size and file operations
import json             # necessary to read json-based data file
import readline         # necessary to be able to auto-complete user
# import webbrowser     # necessary to display web pages
import urllib.request   # necessary to download game data

from rich.console import Console    # necessary for markdown display
from rich.markdown import Markdown  # necessary for markdown display
from zipfile import ZipFile         # necessary for ZIP handling

from room import Room
from objective import Objective
from junction import Junction
from item import Item
from character import Character

cont = 1                # the program will run until this value is set to 0
location = "start"      # the starting room, changes later in the game by walking around

rooms = dict()          # contains all available rooms
objectives = dict()     # contains all available objectives
junctions = dict()      # contains all junctions between the rooms
items = dict()          # contains all available items
characters = dict()     # contains all available side characters

volcab = []             # contains autocomplete values
default_actions = ['beam','cry','exit','grab','help','inspect','look','meditate','phone','quit','recap','scrutinize','talk','walk'] # default actions

console = Console()     # markdown output to console

# all the actions the player can perform
# only triggered once automatically when the player arrives (starts the program) - no command assigned
def arrive():
    display_image("logo")
    print("")
    print("You are arriving at a strange and unknown location.")
    print("You are feeling a little dizzy.")
    rooms[location].visited = True

# get some about information - "scrutinize" command assigned
def scrutinize():
    print("A magical voice whispers into your ear:")
    print("\"This game has been created by Ben Krueger\"")
    print("You wonder what this may mean? You are in a game? Strange thought indeed!")

# triggered automatically when the player enters a wrong command - no command assigned
def lost():
    print("You are feeling lost somehow. You could cry for help to see what happens.")

# shows all available commands - "help" command assigned
def help():
    print("A magical voice whispers into your ear: \"Following commands are available\"")
    print(default_actions)
    print("")
    print("Then it whispers: \"TAB is your friend\"")
    print("You wonder what this TAB may be? A creature? A scroll?")

# set all rooms, objectives, items, etc. to status visited/taken - HIDDEN "cheat" command assigned
def cheat():
    print("Suddenly you hear a rolling thunder all around you. You quickly close your eyes and open them again after a few seconds.")
    print("Has anything happened? No? How strange you think and decide to carry on.")
    for name, room in rooms.items():
        room.visited = True
    for name, objective in objectives.items():
        objective.visited = True
    for name, item in items.items():
        item.visited = True

# have a detailed look what kind of objects a room contains - "inspect" command assigned
def inspect():
    print("You are inspecting the place and looking for further objects you can interact with...")
    print("")

    for name, objective in objectives.items():
        if (objective.location == location):
            print("In this room you can see " + name + ", " + objective.description + ".")
            if (objective.supports == "main"):
                print("    " + name + " seems to know something about a main objective.")
            else:
                print("    " + name + " can you give some hints for the quest " + objective.supports + " is offering.")
            if (objective.visited):
                print("    " + "You already have talked to " + name + " before.")
            else:
                print("    " + "You have not talked to " + name + " yet.")
            print("")

    for name, item in items.items():
        if (item.location == location):
            if (not item.visited):
                print("In a corner you can see a " + name + " lying around. You guess it's a " + item.description + ".")
                print("")

    for name, character in characters.items():
        if (character.location == location):
            print("Furthermore you can see " + name + ", " + character.description)
            print("")

    for name, junction in junctions.items():
        if (junction.location == location):
            print(junction.description + " you can see a junction to " + junction.destination)
            if (rooms[junction.destination].visited):
                print ("    " + "You have visited that location already.")
            else:
                print ("    " + "You have not seen that location yet.")
            print("")

# think about the main quest in the game, triggered automatically when the player arrives - "meditate" command assigned
def meditate():
    print("A quest to save Santa has brought you to this place.")
    print("You think about how all those creatures here could help you.")

# have a quick look at this place - "look" command assigned
def look():
    print("You are currently at " + location + " and admiring what your eyes can see...")
    print("")
    display_image(location)
    print("")
    print(rooms[location].description)

# phone other creatures you already have discovered - "phone" command assigned
def phone():
    # necessary for creature name auto-completion
    global volcab
    new_volcab = []

    print("You put your hand into your right pocket and grab a magical device.")
    print("It has a display where you can see the names of all the creatures you had contact with.")
    print("You guess you can open some channel to a creature by tapping its name.")
    print("")

    # assign all visited creatures to the auto-completion list
    counter = 0
    for name, objective in objectives.items():
        if (objective.visited):
            counter = counter + 1
            new_volcab.append(name)
            print("  Entry: " + name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        name = input("I want to talk to > ")
        if (name in objectives):
            objectives[name].visited = True
            talk_to(name, objectives[name].url)
        else:
            print("")
            print("You decide you don't want to talk right now.")
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
    for name, objective in objectives.items():
        if (objective.location == location):
            counter = counter + 1
            new_volcab.append(name)
            print("  Entry: " + name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        name = input("I want to talk to > ")
        if (name in objectives):
            objectives[name].visited = True
            talk_to(name, objectives[name].url)
        else:
            print("")
            print("You decide you don't want to talk right now.")
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
    print("")

    # assign all visited rooms to the auto-completion list
    counter = 0
    for name, room in rooms.items():
        if (room.visited):
            counter = counter + 1
            new_volcab.append(name)
            print("  Entry: " + name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        destination = input("I want to go to > ")
        if (location != destination and destination in rooms):
            print("")
            print("You are going to " + destination)
            location = destination
        else:
            print("")
            print("You decide to stay where you currently are.")
    else:
        print("After a moment you realize you have not been anywhere yet.")
    set_default_complete()

# walk to other places - "walk" command assigned
def walk():
    # necessary for room name auto-completion and new room selection
    global volcab
    global location
    new_volcab = []

    # assign all connected rooms to the auto-completion list
    counter = 0
    for id, junction in junctions.items():
        if (junction.location == location):
            counter = counter + 1
            new_volcab.append(junction.destination)
            print("  Entry: " + junction.destination)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print ("")
        destination = input("I want to go to > ")
        if (location != destination and destination in rooms):
            print("")
            print("You are going to " + destination)
            location = destination
            rooms[destination].visited = True
        else:
            print("")
            print("You decide to stay where you currently are.")
    else:
        print("After a moment you realize there is no way out of this room.")
    set_default_complete()

# grab an item - "grab" command assigned
def grab():
    # necessary for item name auto-completion
    global volcab
    new_volcab = []

    # assign all items in this room to the auto-completion list
    counter = 0
    for name, item in items.items():
        if (item.location == location and item.visited is not True):
            counter = counter + 1
            new_volcab.append(name)
            print("  Entry: " + name)

    if (counter > 0):
        set_custom_complete(new_volcab)
        print("")
        name = input("I want to grab > ")
        if (name in items):
            items[name].visited = True
            print("")
            print("You grab the " + name + " and put it into your bag.")
        else:
            print("")
            print("You decide you don't want to grab anything right now.")
    else:
        print("After a moment you realize no items can be found in this room.")
    set_default_complete()

# check everything you have encountered - "recap" command assigned
def recap():
    counter_r = 0
    counter_o = 0
    counter_i = 0
    for name, room in rooms.items():
        if (room.visited):
            counter_r = counter_r + 1
    for name, objective in objectives.items():
        if (objective.visited):
            counter_o = counter_o + 1
    for name, item in items.items():
        if (item.visited):
            counter_i = counter_i + 1
    print("You have visited " + str(counter_r) + " room(s). You feel like there is/are " + str(len(rooms) - counter_r) + " more to discover.")
    print("You have talked to " + str(counter_o) + " creature(s). You guess there is/are " + str(len(objectives) - counter_o) + " more waiting for contact.")
    print("You have grabbed " + str(counter_i) + " item(s). Maybe you can put " + str(len(items) - counter_i) + " additional one(s) into your bag.")
    
# helper functions, cannot be triggered by the player directly
# resets the auto-completion to the default actions list
def set_default_complete():
    global volcab
    volcab = default_actions

# sets the auto-completion list to a custom one (necessary for creature and room auto-completion)
def set_custom_complete(list):
    global volcab
    volcab = list

# basic yes no question
def yesno():
    answer = input("You are saying yes or no > ")
    if (answer == "yes" or answer == "y"):
        return True
    else:
        return False

# talk to a creature
def talk_to(name, url):
    print("You are talking to " + name)
    display_image(name)

    if (objectives[name].requires != "none" and not items[objectives[name].requires].visited):
        print("")
        print(name + " asks for a " + objectives[name].requires + ". Sadly you can't find it in your bag.")
    else:
        print("")
        print(name + " gives you following quest:")
        display_markdown(name + "_q")
                        
        print("")
        print(name + " asks you if you want to open this quest.")
        if (yesno()):
            # webbrowser.open(url, new=1)
            print("")
            print(url)

        print("")
        print("After a short while " + name + " also offers you the solution.")
        print("Do you want to hear it?")
        if (yesno()):
            display_markdown(name + "_a")

# auto-completion with Python readline, requires readline
def complete(text,state):
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

# displays a colored ANSII image, depending on the terminal size, requires external program
def display_image(image_name):
    try:
        f = open("images/" + image_name + ".jpg","r")
        os.system("/bin/jp2a " + "images/" + image_name + ".jpg --colors --fill --color-depth=8")
        f.close()
        return (True)
    except IOError:
        print("Image file not found for " + image_name)
        return (False)

# displays a markdown page
def display_markdown(md_name):
    try:
        f = open("quests/" + md_name + ".md","r")
        md = Markdown(f.read())
        console.print(md)
        f.close()
        return (True)
    except IOError:
        print("Markdown file not found for " + md_name)
        return (False)

# parses the JSON based configuration file and creature objects from that configuration, requires json
def load_data():
    url = 'https://github.com/benjamin-bk-krueger/2021-kringlecon/raw/main/2021-kringlecon.zip'
    urllib.request.urlretrieve(url, r'./gamedata.zip')
    with ZipFile('./gamedata.zip', 'r') as zip:
        zip.extractall()

    global location
    counter = 1
    counter_loaded = 0
    f = open("data.json")
    data = json.load(f)
    for i in data["rooms"]:
        room = Room()
        room.description = i["description"]
        rooms.update({i["name"]: room})
        counter_loaded = counter_loaded + 1

        # the first room is the starting location
        if (location == "start"):
            location = i["name"]
        
        # load all items in the room
        try:
            for j in i["items"]:
                item = Item()
                item.description = j["description"]
                item.location = i["name"]
                items.update({j["name"]: item})
                counter_loaded = counter_loaded + 1
        except:
            pass
        
        # load all characters in the room
        try:
            for j in i["characters"]:
                character = Character()
                character.description = j["description"]
                character.location = i["name"]
                characters.update({j["name"]: character})
                counter_loaded = counter_loaded + 1
        except:
            pass

        # load all objectives in the room
        try:
            for j in i["objectives"]:
                objective = Objective()
                objective.description = j["description"]
                objective.location = i["name"]
                objective.difficulty = j["difficulty"]
                objective.url = j["url"]
                objective.supports = j["supports"]
                objective.requires = j["requires"]
                objectives.update({j["name"]: objective})
                counter_loaded = counter_loaded + 1
        except:
            pass

        # load all junctions in the room
        try:
            for j in i["junctions"]:
                junction = Junction()
                junction.destination = j["destination"]
                junction.description = j["description"]
                junction.location = i["name"]
                junctions.update({counter: junction})
                counter = counter + 1
                counter_loaded = counter_loaded + 1
        except:
            pass
    f.close()
    return(counter_loaded)

# queries the user to enter a command and triggers the matching function
def query_user():
    global cont
    print("")
    cmd = input("I want to > ")
    print("")
    if (cmd == "help"):
        help()
    if (cmd == "cheat"):
        cheat()
    elif (cmd == "cry"):
        help()
    elif (cmd == "beam"):
        beam()
    elif (cmd == "exit"):
        cont = 0
    elif (cmd == "grab"):
        grab()
    elif (cmd == "inspect"):
        inspect()
    elif (cmd == "look"):
        look()
    elif (cmd == "meditate"):
        meditate()
    elif (cmd == "recap"):
        recap()
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
readline.parse_and_bind("tab: complete") # Linux
#readline.parse_and_bind ("bind ^I rl_complete") # Mac
readline.set_completer(complete)

if __name__ == '__main__':
    # open the JSON data file and build all object dictionnaries
    load_data()

    # start the game until the player decides to quit
    print("")
    arrive()
    print("")
    meditate()

    while (cont == 1):
        query_user()
else:
    print(f"Cannot be run as module import: {__name__}")
