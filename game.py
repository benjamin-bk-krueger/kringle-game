import os               # necessary to access terminal size and file operations
import json             # necessary to read json-based data file
import readline         # necessary to be able to auto-complete user
# import webbrowser     # necessary to display web pages
import urllib.request   # necessary to download game data
import shutil           # necessary to recursively delete files
import psycopg2         # necessary to connect to PostGreSQL database

from rich.console import Console    # necessary for markdown display
from rich.markdown import Markdown  # necessary for markdown display
from zipfile import ZipFile         # necessary for ZIP handling
from psycopg2 import Error          # necessary for DB error handling

from room import Room
from objective import Objective
from junction import Junction
from item import Item
from character import Character
from colors import bcolors

cont = 1                # the program will run until this value is set to 0
location = 0            # the starting room, changes later in the game by walking around

rooms = dict()          # contains all available rooms
objectives = dict()     # contains all available objectives
junctions = dict()      # contains all junctions between the rooms
items = dict()          # contains all available items
characters = dict()     # contains all available side characters

volcab = []             # contains autocomplete values
default_actions = ['beam','cry','exit','grab','inspect','look','meditate','phone','question','recap','talk','walk'] # default actions

console = Console()     # markdown output to console

gamedata = os.environ['HOME'] + "/.kringlecon"  # directory for game data
gameurl = 'https://white.blk8.de/kringle_gamedata/2021-kringlecon.zip' # url for game data

creator_name = 'BenKrueger'
world_name = 'KringleCon2021'

# all the actions the player can perform
# only triggered once automatically when the player arrives (starts the program) - no command assigned
def arrive():
    display_image("logo")
    print("")
    print (f"You are arriving at a {bcolors.HEADER}strange and unknown location{bcolors.ENDC}.")
    print("You are feeling a little dizzy.")
    print(f"What should be your {bcolors.GREENFG}next steps{bcolors.ENDC}? You are pausing for a moment.")
    rooms[location].visited = True

# get some about information - "scrutinize" command assigned
def question():
    print("A low voice whispers into your ear:")
    print(f"{bcolors.YELLOWFG}This game has been created by Ben Krueger{bcolors.ENDC}")
    print("You wonder what this may mean? You are inside a game? Strange thought indeed!")

# triggered automatically when the player enters a wrong command - no command assigned
def lost():
    print(f"You are {bcolors.HEADER}feeling lost{bcolors.ENDC} somehow. You could {bcolors.GREENFG}cry{bcolors.ENDC} for help to see what happens.")

# shows all available commands - "help" command assigned
def help():
    print(f"A low voice whispers into your ear: {bcolors.YELLOWFG}Following commands are available:{bcolors.ENDC}")
    for i in default_actions:
        print(bcolors.BOLD + i[0:1] + bcolors.ENDC, end ="")
        print(i[1:], end =", ")
    print("")
    print("")
    print(f"Then it whispers: {bcolors.YELLOWFG}TAB is your friend{bcolors.ENDC}")
    print(f"You wonder what this {bcolors.GREENFG}TAB{bcolors.ENDC} may be? A creature? An item?")

# set all rooms, objectives, items, etc. to status visited/taken - HIDDEN "cheat" command assigned
def cheat():
    print(f"Suddenly you hear a {bcolors.HEADER}rolling thunder{bcolors.ENDC} all around you. You quickly close your eyes and open them again after a few seconds.")
    print(f"{bcolors.GREENFG}Has anything happened{bcolors.ENDC}? No? How strange you think and decide to carry on.")
    for id, room in rooms.items():
        room.visited = True
    for id, objective in objectives.items():
        objective.visited = True
    for id, item in items.items():
        item.visited = True

# fetch the configuration again from the default URL - HIDDEN "urlrefresh" command assigned
def refresh_data():
    print(f"You turn around and {bcolors.HEADER}clap your hands{bcolors.ENDC} three times.")
    print(f"What is, has passed. {bcolors.GREENFG}What could be, will happen{bcolors.ENDC}.") 
    shutil.rmtree(gamedata)
    os.mkdir(gamedata) 
    urllib.request.urlretrieve(gameurl, gamedata + "/gamedata.zip")
    with ZipFile(gamedata + "/gamedata.zip", 'r') as zip:
        zip.extractall(gamedata)

# have a detailed look what kind of objects a room contains - "inspect" command assigned
def inspect():
    print(f"You are {bcolors.HEADER}inspecting the place{bcolors.ENDC} and looking for further objects you can interact with...")
    print("")

    for id, objective in objectives.items():
        if (objective.location == location):
            print(f"In this room you can see {bcolors.BLUEFG}{objective.name}{bcolors.ENDC} {objective.description}.")
            if (objective.supportedby != "none"):
                print(f"|- {objective.supportedby} can you give some hints for this quest.")
            if (objective.visited):
                print(f"`- You {bcolors.GREENFG}already have talked{bcolors.ENDC} to {objective.name} before.")
            else:
                print(f"`- You have {bcolors.REDFG}not talked{bcolors.ENDC} to {objective.name} yet.")
            print("")

    for id, item in items.items():
        if (item.location == location):
            if (not item.visited):
                print(f"In a corner you can see a {bcolors.BLUEFG}{item.name}{bcolors.ENDC} lying around. You guess it's a {item.description}.")
                print("")

    for id, character in characters.items():
        if (character.location == location):
            print(f"Furthermore you can see {bcolors.BLUEFG}{character.name}{bcolors.ENDC} {character.description}")
            print("")

    for id, junction in junctions.items():
        if (junction.location == location):
            print(f"{junction.description} you can see a junction to {bcolors.BLUEFG}{rooms[junction.destination].name}{bcolors.ENDC}.")
            if (rooms[junction.destination].visited):
                print (f"`- You {bcolors.GREENFG}have visited{bcolors.ENDC} that location already.")
            else:
                print (f"`- You {bcolors.REDFG}have not seen{bcolors.ENDC} that location yet.")

# think about the main quest in the game, triggered automatically when the player arrives - "meditate" command assigned
def meditate():
    print(f"A quest to {bcolors.HEADER}save Santa{bcolors.ENDC} has brought you to this place.")
    print("You think about how all those characters here could help you.")

# have a quick look at this place - "look" command assigned
def look():
    print(f"You are currently at {bcolors.BLUEFG}{rooms[location].name}{bcolors.ENDC} and {bcolors.HEADER}admiring{bcolors.ENDC} what your eyes can see...")
    print("")
    display_image(rooms[location].name)
    print(rooms[location].description)

# phone other creatures you already have discovered - "phone" command assigned
def phone():
    print(f"You put your hand into your right pocket and {bcolors.HEADER}grab a magical device{bcolors.ENDC}.")
    print("It has a display where you can see the names of all the creatures you had contact with.")
    print(f"You guess you can {bcolors.GREENFG}open some channel{bcolors.ENDC} to a creature by tapping its name.")

    # assign all visited creatures to the auto-completion list
    counter = 0
    for id, objective in objectives.items():
        if (objective.visited):
            counter = counter + 1
            print(f"|- {name}")

    if (counter > 0):
        print("")
        namefull = input(f"{bcolors.GREYBG}I want to talk to ---->{bcolors.ENDC} ")
        try:
            name = int(namefull)
        except:
            name = 0
        if (name in objectives):
            objectives[name].visited = True
            talk_to(name)
        else:
            print("")
            print(f"You decide you {bcolors.REDFG}don't want to talk{bcolors.ENDC} right now.")
    else:
        print("")
        print(f"After a moment you realize you have {bcolors.REDFG}not met anyone{bcolors.ENDC} yet.")
    set_default_complete()
    
# talk to other creatures - "talk" command assigned
def talk():
    print(f"You {bcolors.HEADER}look around{bcolors.ENDC} for other characters in this room.")

    # assign all creatures in this room to the auto-completion list
    counter = 0
    for id, objective in objectives.items():
        if (objective.location == location):
            counter = counter + 1
            print(f"|- [{id}] {objective.name}")

    if (counter > 0):
        print("")
        namefull = input(f"{bcolors.GREYBG}I want to talk to ---->{bcolors.ENDC} ")
        try:
            name = int(namefull)
        except:
            name = 0
        if (name in objectives):
            objectives[name].visited = True
            talk_to(name)
        else:
            print("")
            print(f"You decide you {bcolors.REDFG}don't want to talk{bcolors.ENDC} right now.")
    else:
        print("")
        print(f"After a moment you realize {bcolors.REDFG}no one is in this room{bcolors.ENDC}.")
    set_default_complete()

# beam to places you already have discovered - "beam" command assigned
def beam():
    # necessary for room name auto-completion and new room selection
    global location

    print(f"You put your hand into your left pocket and {bcolors.HEADER}grab a magical device{bcolors.ENDC}.")
    print("It has a display where you can see the names of all the places you have visited.")
    print(f"You guess you can {bcolors.GREENFG}travel there{bcolors.ENDC} by tapping its name.")

    # assign all visited rooms to the auto-completion list
    counter = 0
    for id, room in rooms.items():
        if (room.visited):
            counter = counter + 1
            print(f"|- [{id}] {room.name}")

    if (counter > 0):
        print("")
        dest = input(f"{bcolors.GREYBG}I want to go to ------>{bcolors.ENDC} ")
        try:
            destination = int(dest)
        except:
            destination = 0
        if (location != destination and destination in rooms):
            print("")
            print(f"You are {bcolors.GREENFG}going to{bcolors.ENDC} {rooms[destination].name}")
            location = destination
        else:
            print("")
            print(f"You decide to {bcolors.REDFG}stay{bcolors.ENDC} where you currently are.")
    else:
        print("")
        print(f"After a moment you realize you {bcolors.REDFG}have not been anywhere yet{bcolors.ENDC}.")
    set_default_complete()

# walk to other places - "walk" command assigned
def walk():
    # necessary for room name auto-completion and new room selection
    global location

    print(f"You {bcolors.HEADER}look around{bcolors.ENDC} for other places to reach.")

    # assign all connected rooms to the auto-completion list
    counter = 0
    for id, junction in junctions.items():
        if (junction.location == location):
            counter = counter + 1
            print(f"|- [{junction.destination}] {rooms[junction.destination].name}")

    if (counter > 0):
        print ("")
        dest = input(f"{bcolors.GREYBG}I want to go to ------>{bcolors.ENDC} ")
        try:
            destination = int(dest)
        except:
            destination = 0
        if (location != destination and destination in rooms):
            print("")
            print(f"You are {bcolors.GREENFG}going to{bcolors.ENDC} {rooms[destination].name}")
            location = destination
            rooms[destination].visited = True
        else:
            print("")
            print(f"You decide to {bcolors.REDFG}stay{bcolors.ENDC} where you currently are.")
    else:
        print(f"After a moment you realize there is {bcolors.REDFG}no way out{bcolors.ENDC} of this room.")
    set_default_complete()

# grab an item - "grab" command assigned
def grab():
    print(f"You {bcolors.HEADER}look around{bcolors.ENDC} for things to grab.")

    # assign all items in this room to the auto-completion list
    counter = 0
    for id, item in items.items():
        if (item.location == location and item.visited is not True):
            counter = counter + 1
            print(f"|- [{id}] {item.name}")

    if (counter > 0):
        print("")
        idname = input(f"{bcolors.GREYBG}I want to grab ------->{bcolors.ENDC} ")
        try:
            id = int(idname)
        except:
            id = 0
        if (id in items):
            items[id].visited = True
            print("")
            print(f"You grab the {items[id].name} and {bcolors.GREENFG}put it into your bag{bcolors.ENDC}.")
        else:
            print("")
            print(f"You decide you {bcolors.REDFG}don't want to grab{bcolors.ENDC} anything right now.")
    else:
        print("")
        print(f"After a moment you realize {bcolors.REDFG}no items can be found{bcolors.ENDC} in this room.")
    set_default_complete()

# check everything you have encountered - "recap" command assigned
def recap():
    counter_r = 0
    counter_o = 0
    counter_i = 0
    for id, room in rooms.items():
        if (room.visited):
            counter_r = counter_r + 1
    for id, objective in objectives.items():
        if (objective.visited):
            counter_o = counter_o + 1
    for id, item in items.items():
        if (item.visited):
            counter_i = counter_i + 1
    print(f"You {bcolors.HEADER}have visited{bcolors.ENDC} {str(counter_r)} room(s). You feel like there is/are {str(len(rooms) - counter_r)} more to discover.")
    print(f"You {bcolors.HEADER}have talked{bcolors.ENDC} to {str(counter_o)} creature(s). You guess there is/are {str(len(objectives) - counter_o)} more waiting for contact.")
    print(f"You {bcolors.HEADER}have grabbed{bcolors.ENDC} {str(counter_i)} item(s). Maybe you can put {str(len(items) - counter_i)} additional one(s) into your bag.")
    
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
    answer = input(f"{bcolors.GREYBG}I am saying yes ------>{bcolors.ENDC} ")
    if (answer == "yes" or answer == "y"):
        return True
    else:
        return False

# talk to a character
def talk_to(name):
    print("")
    print(f"You are talking to {bcolors.BLUEFG}{objectives[name].name}{bcolors.ENDC}")
    display_image(objectives[name].name)

    if (objectives[name].requires != "none" and not items[objectives[name].requires].visited):
        print("")
        print(f"{bcolors.BLUEFG}{objectives[name].name}{bcolors.ENDC} asks for a {bcolors.BLUEFG}{objectives[name].requires}{bcolors.ENDC}. Sadly you can't find it in your bag.")
    else:
        print("")
        print(f"{bcolors.BLUEFG}{objectives[name].name}{bcolors.ENDC} gives you following quest:")
        print("")
        display_quest(name)
                        
        print("")
        print(f"{bcolors.BLUEFG}{objectives[name].name}{bcolors.ENDC} asks you if you want to open this quest.")
        print("")
        if (yesno()):
            # webbrowser.open(url, new=1)
            print("")
            print(objectives[name].url)

        print("")
        print(f"After a short while {bcolors.BLUEFG}{objectives[name].name}{bcolors.ENDC} also offers you the solution.")
        print("Do you want to hear it?")
        print("")
        if (yesno()):
            print("")
            display_solution(name)

# auto-completion with Python readline, requires readline
def complete(text,state):
    results = [x for x in volcab if x.startswith(text)] + [None]
    return results[state]

# displays a colored ANSII image, depending on the terminal size, requires external program
def display_image(image_name):
    try:
        #f = open(gamedata + "/images/" + image_name + ".jpg","r")
        os.system("/bin/jp2a \"" + gamedata + "/images/" + image_name + ".jpg\" --colors --fill --color-depth=8")
        #f.close()
        return (True)
    except IOError:
        print(f"Image file not found for {image_name}")
        return (False)

# displays a quest markdown page
def display_quest(md_name):
    creator = fetch_one_from_db(f'SELECT * FROM creator where creator_name = \'{creator_name}\';')
    creator_id = creator[0]

    quest = fetch_one_from_db(f'SELECT * FROM quest where objective_id = {md_name} and creator_id = {creator_id};')
    if (quest!= None):
        md = Markdown(str(bytes(quest[3]), 'utf-8'))
        console.print(md)
    else:
        console.print ("No quest entry found.")

# displays a solution markdown page
def display_solution(md_name):
    creator = fetch_one_from_db(f'SELECT * FROM creator where creator_name = \'{creator_name}\';')
    creator_id = creator[0]

    quest = fetch_one_from_db(f'SELECT * FROM solution where objective_id = {md_name} and creator_id = {creator_id};')
    if (quest!= None):
        md = Markdown(str(bytes(quest[3]), 'utf-8'))
        console.print(md)
    else:
        console.print ("No solution entry found.")

# open a connection to PostgreSQL DB and return the connection
def get_db_connection():
    try:
        conn = psycopg2.connect(user="kringle",
                                    password="kringle",
                                    host="kringle_database",
                                    port="5432",
                                    database="kringle")
        return conn
    except (Exception, Error) as error:
        return None

# fetch all rows from a query
def fetch_all_from_db(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# fetch only a single row from a query
def fetch_one_from_db(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

# update one row from a query
def update_one_in_db(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    cur.close()
    conn.commit()
    conn.close()

# parses the JSON based configuration file and creature objects from that configuration, requires json
def load_data():
    global location
    counter_loaded = 0

    record = fetch_one_from_db("SELECT version();")
    print("You are connected to - ", record, "\n")

    world = fetch_one_from_db(f'SELECT * FROM world WHERE world_name = \'{world_name}\';')
    world_id = world[0]

    room_records = fetch_all_from_db(f"SELECT * FROM room WHERE world_id = {world_id};")
    for i in room_records:
        room = Room()
        room.name = i[2]
        room.description = i[3]
        rooms.update({i[0]: room})
        counter_loaded = counter_loaded + 1

        # the first room is the starting location
        if (location == 0):
            location = i[0]

    item_records = fetch_all_from_db(f"select * from item WHERE world_id = {world_id};")
    for i in item_records:
        item = Item()
        item.name = i[3]
        item.description = i[4]
        item.location = i[1]
        items.update({i[0]: item})
        counter_loaded = counter_loaded + 1
        
    person_records = fetch_all_from_db(f"select * from person WHERE world_id = {world_id};")
    for i in person_records:
        character = Character()
        character.name = i[3]
        character.description = i[4]
        character.location = i[1]
        characters.update({i[0]: character})
        counter_loaded = counter_loaded + 1

    objective_records = fetch_all_from_db(f"select * from objective WHERE world_id = {world_id};")
    for i in objective_records:
        objective = Objective()
        objective.name = i[3]
        objective.description = i[4]
        objective.location = i[1]
        objective.difficulty = i[5]
        objective.url = i[6]
        objective.supportedby = i[7]
        objective.requires = i[8]
        objectives.update({i[0]: objective})
        counter_loaded = counter_loaded + 1

    junction_records = fetch_all_from_db(f"select * from junction WHERE world_id = {world_id};")
    for i in junction_records:
        junction = Junction()
        junction.destination = i[3]
        junction.location = i[1]    
        junction.description = i[4]
        junctions.update({i[0]: junction})
        counter_loaded = counter_loaded + 1

    return(counter_loaded)

# queries the user to enter a command and triggers the matching function
def query_user():
    global cont
    print("")
    cmd = input(f"{bcolors.GREYBG}I want to ------------>{bcolors.ENDC} ")
    print("")
    if (cmd == "cheat"):
        cheat()
    elif (cmd == "cry" or cmd == "c"):
        help()
    elif (cmd == "beam" or cmd == "b"):
        beam()
    elif (cmd == "exit" or cmd == "e"):
        cont = 0
    elif (cmd == "grab" or cmd == "g"):
        grab()
    elif (cmd == "inspect") or cmd == "i":
        inspect()
    elif (cmd == "look" or cmd == "l"):
        look()
    elif (cmd == "meditate" or cmd == "m"):
        meditate()
    elif (cmd == "recap" or cmd == "r"):
        recap()
    elif (cmd == "talk" or cmd == "t"):
        talk()
    elif (cmd == "phone" or cmd == "p"):
        phone()
    elif (cmd == "urlrefresh"):
        refresh_data()
    elif (cmd == "question" or cmd == "q"):
        question()
    elif (cmd == "walk" or cmd == "w"):
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
    if len(rooms) > 0:
        print("")
        arrive()
        print("")
        meditate()
    else:
        print("")
        print("You are looking at a green field.")

    while (cont == 1):
        query_user()
else:
    print(f"Cannot be run as module import: {__name__}")
