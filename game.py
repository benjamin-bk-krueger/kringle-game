import os  # necessary to access terminal size and file operations
import readline  # necessary to be able to auto-complete user
# import urllib.request  # necessary to download game data
# import shutil  # necessary to recursively delete files
import psycopg2  # necessary to connect to PostGreSQL database

from rich.console import Console  # necessary for markdown display
from rich.markdown import Markdown  # necessary for markdown display
# from zipfile import ZipFile  # necessary for ZIP handling
from psycopg2 import Error  # necessary for DB error handling

from room import Room
from objective import Objective
from junction import Junction
from item import Item
from character import Character
from colors import Bcolors

cont = 1  # the program will run until this value is set to 0
location = 0  # the starting room, changes later in the game by walking around

rooms = dict()  # contains all available rooms
objectives = dict()  # contains all available objectives
junctions = dict()  # contains all junctions between the rooms
items = dict()  # contains all available items
characters = dict()  # contains all available side characters

vocabulary = []  # contains autocomplete values
default_actions = ['beam', 'cry', 'exit', 'grab', 'inspect', 'look', 'meditate', 'phone', 'question', 'recap', 'talk',
                   'walk']  # default actions

console = Console()  # markdown output to console

game_data = os.environ['HOME'] + "/.kringlecon"  # directory for game data

creator_name = 'BenKrueger'
world_name = 'KringleCon2021'


# all the actions the player can perform
# only triggered once automatically when the player arrives (starts the program) - no command assigned
def arrive():
    display_image("logo")
    print("")
    print("You are arriving at a " + color_header("strange and unknown location") + ".")
    print("You are feeling a little dizzy.")
    print("What should be your " + color_ok("next steps") + "? You are pausing for a moment.")
    rooms[location].visited = True


# get some about information - "scrutinize" command assigned
def question():
    print("A low voice whispers into your ear:")
    print(color_warning("This game has been created by Ben Krueger"))
    print("You wonder what this may mean? You are inside a game? Strange thought indeed!")


# triggered automatically when the player enters a wrong command - no command assigned
def lost():
    print("You are " + color_header("feeling lost") + " somehow. You could " + color_ok("cry") +
          " for help to see what happens.")


# shows all available commands - "help" command assigned
def cry():
    print("A low voice whispers into your ear: " + color_warning("Following commands are available:"))
    for i in default_actions:
        print(Bcolors.BOLD + i[0:1] + Bcolors.ENDC, end="")
        print(i[1:], end=", ")
    print("")
    print("")
    print("Then it whispers: " + color_warning("TAB is your friend"))
    print("You wonder what this " + color_ok("TAB") + " may be? A creature? An item?")


# set all rooms, objectives, items, etc. to status visited/taken - HIDDEN "cheat" command assigned
def cheat():
    print("Suddenly you hear a " + color_header("rolling thunder") + " all around you. You quickly close " +
          "your eyes and open them again after a few seconds.")
    print(color_ok("Has anything happened") + "? No? How strange you think and decide to carry on.")
    for room_id, room in rooms.items():
        room.visited = True
    for objective_id, objective in objectives.items():
        objective.visited = True
    for item_id, item in items.items():
        item.visited = True


# have a detailed look what kind of objects a room contains - "inspect" command assigned
def inspect():
    print("You are " + color_header("inspecting the place") + " and looking for further objects you can " +
          "interact with...")
    print("")

    for objective_id, objective in objectives.items():
        if objective.location == location:
            print("In this room you can see " + color_object(objective.name) + objective.description + ".")
            if objective.supportedby != "none":
                print("|- " + objective.supportedby + " can you give some hints for this quest.")
            if objective.visited:
                print("`- You " + color_ok("already have talked") + " to " + objective.name + " before.")
            else:
                print("`- You have " + color_alert("not talked") + " to " + objective.name + " yet.")
            print("")

    for item_id, item in items.items():
        if item.location == location:
            if not item.visited:
                print("In a corner you can see a " + color_object(item.name) + " lying around. You guess it's a " +
                      item.description + ".")
                print("")

    for character_id, character in characters.items():
        if character.location == location:
            print("Furthermore you can see " + color_object(character.name) + " " + character.description)
            print("")

    for junction_id, junction in junctions.items():
        if junction.location == location:
            print(junction.description + " you can see a junction to " +
                  color_object(rooms[junction.destination].name) + ".")
            if rooms[junction.destination].visited:
                print("`- You " + color_ok("have visited") + " that location already.")
            else:
                print("`- You " + color_alert("have not seen") + " that location yet.")


# think about the main quest in the game, triggered automatically when the player arrives - "meditate" command assigned
def meditate():
    print("A quest to " + color_header("save Santa") + " has brought you to this place.")
    print("You think about how all those characters here could help you.")


# have a quick look at this place - "look" command assigned
def look():
    print("You are currently at " + color_object(rooms[location].name) + " and " + color_header("admiring") +
          " what your eyes can see...")
    print("")
    display_image(rooms[location].name)
    print(rooms[location].description)


# phone other creatures you already have discovered - "phone" command assigned
def phone():
    print("You put your hand into your right pocket and " + color_header("grab a magical device") + ".")
    print("It has a display where you can see the names of all the creatures you had contact with.")
    print("You guess you can " + color_ok("open some channel") + " to a creature by tapping its name.")

    # assign all visited creatures to the auto-completion list
    counter = 0
    for objective_id, objective in objectives.items():
        if objective.visited:
            counter = counter + 1
            print(f"|- [{objective_id}] {objective.name}")

    if counter > 0:
        print("")
        id_text = input(color_notice("I want to talk to ---->") + " ")
        try:
            objective_id = int(id_text)
        except ValueError:
            objective_id = 0
        if objective_id in objectives:
            objectives[objective_id].visited = True
            talk_to(objective_id)
        else:
            print("")
            print("You decide you " + color_alert("don't want to talk") + " right now.")
    else:
        print("")
        print("After a moment you realize you have " + color_alert("not met anyone") + " yet.")
    set_default_complete()


# talk to other creatures - "talk" command assigned
def talk():
    print("You " + color_header("look around") + " for other characters in this room.")

    # assign all creatures in this room to the auto-completion list
    counter = 0
    for objective_id, objective in objectives.items():
        if objective.location == location:
            counter = counter + 1
            print(f"|- [{objective_id}] {objective.name}")

    if counter > 0:
        print("")
        id_text = input(color_notice("I want to talk to ---->") + " ")
        try:
            objective_id = int(id_text)
        except ValueError:
            objective_id = 0
        if objective_id in objectives:
            objectives[objective_id].visited = True
            talk_to(objective_id)
        else:
            print("")
            print("You decide you " + color_alert("don't want to talk") + " right now.")
    else:
        print("")
        print("After a moment you realize " + color_alert("no one is in this room") + ".")
    set_default_complete()


# beam to places you already have discovered - "beam" command assigned
def beam():
    # necessary for room name auto-completion and new room selection
    global location

    print("You put your hand into your left pocket and " + color_header("grab a magical device") + ".")
    print("It has a display where you can see the names of all the places you have visited.")
    print("You guess you can " + color_ok("travel there") + " by tapping its name.")

    # assign all visited rooms to the auto-completion list
    counter = 0
    for room_id, room in rooms.items():
        if room.visited:
            counter = counter + 1
            print(f"|- [{room_id}] {room.name}")

    if counter > 0:
        print("")
        dest = input(color_notice("I want to go to ------>") + " ")
        try:
            destination = int(dest)
        except ValueError:
            destination = 0
        if location != destination and destination in rooms:
            print("")
            print("You are " + color_ok("going to") + " " + rooms[destination].name)
            location = destination
        else:
            print("")
            print("You decide to " + color_alert("stay") + " where you currently are.")
    else:
        print("")
        print("After a moment you realize you " + color_alert("have not been anywhere yet") + ".")
    set_default_complete()


# walk to other places - "walk" command assigned
def walk():
    # necessary for room name auto-completion and new room selection
    global location

    print("You " + color_header("look around") + " for other places to reach.")

    # assign all connected rooms to the auto-completion list
    counter = 0
    for junction_id, junction in junctions.items():
        if junction.location == location:
            counter = counter + 1
            print(f"|- [{junction.destination}] {rooms[junction.destination].name}")

    if counter > 0:
        print("")
        dest = input(color_notice("I want to go to ------>") + " ")
        try:
            destination = int(dest)
        except ValueError:
            destination = 0
        if location != destination and destination in rooms:
            print("")
            print("You are " + color_ok("going to") + " " + rooms[destination].name)
            location = destination
            rooms[destination].visited = True
        else:
            print("")
            print("You decide to " + color_alert("stay") + " where you currently are.")
    else:
        print("After a moment you realize there is " + color_alert("no way out") + " of this room.")
    set_default_complete()


# grab an item - "grab" command assigned
def grab():
    print("You " + color_header("look around") + " for things to grab.")

    # assign all items in this room to the auto-completion list
    counter = 0
    for item_id, item in items.items():
        if item.location == location and item.visited is not True:
            counter = counter + 1
            print(f"|- [{item_id}] {item.name}")

    if counter > 0:
        print("")
        id_text = input(f"{Bcolors.GREYBG}I want to grab ------->{Bcolors.ENDC} ")
        try:
            item_id = int(id_text)
        except ValueError:
            item_id = 0
        if item_id in items:
            items[item_id].visited = True
            print("")
            print("You grab the " + items[item_id].name + " and " + color_ok("put it into your bag") + ".")
        else:
            print("")
            print("You decide you " + color_alert("don't want to grab") + " anything right now.")
    else:
        print("")
        print("After a moment you realize " + color_alert("no items can be found") + " in this room.")
    set_default_complete()


# check everything you have encountered - "recap" command assigned
def recap():
    counter_r = 0
    counter_o = 0
    counter_i = 0
    for room_id, room in rooms.items():
        if room.visited:
            counter_r = counter_r + 1
    for objective_id, objective in objectives.items():
        if objective.visited:
            counter_o = counter_o + 1
    for item_id, item in items.items():
        if item.visited:
            counter_i = counter_i + 1
    print("You " + color_header("have visited") + str(counter_r) + " room(s). You feel like there is/are " +
          str(len(rooms) - counter_r) + " more to discover.")
    print("You " + color_header("have talked") + " to " + str(counter_o) + " creature(s). You guess there is/are " +
          str(len(objectives) - counter_o) + " more waiting for contact.")
    print("You " + color_header("have grabbed") + str(counter_i) + " item(s). Maybe you can put " +
          str(len(items) - counter_i) + " additional one(s) into your bag.")


# helper functions, cannot be triggered by the player directly
# resets the auto-completion to the default actions list
def set_default_complete():
    global vocabulary
    vocabulary = default_actions


# sets the auto-completion list to a custom one (necessary for creature and room auto-completion)
def set_custom_complete(word_list):
    global vocabulary
    vocabulary = word_list


# auto-completion with Python readline, requires readline
def auto_complete(text, state):
    results = [x for x in vocabulary if x.startswith(text)] + [None]
    return results[state]


# terminal colors
def color_notice(terminal_text):
    return f"{Bcolors.GREYBG}{terminal_text}{Bcolors.ENDC}"


def color_object(terminal_text):
    return f"{Bcolors.BLUEFG}{terminal_text}{Bcolors.ENDC}"


def color_header(terminal_text):
    return f"{Bcolors.HEADER}{terminal_text}{Bcolors.ENDC}"


def color_ok(terminal_text):
    return f"{Bcolors.GREENFG}{terminal_text}{Bcolors.ENDC}"


def color_warning(terminal_text):
    return f"{Bcolors.YELLOWFG}{terminal_text}{Bcolors.ENDC}"


def color_alert(terminal_text):
    return f"{Bcolors.REDFG}{terminal_text}{Bcolors.ENDC}"


# basic yes no question
def yesno():
    answer = input(color_notice("I am saying yes ------>") + " ")
    if answer == "yes" or answer == "y":
        return True
    else:
        return False


# talk to a character
def talk_to(objective_id):
    print("")
    print("You are talking to " + color_object(objectives[objective_id].name))
    display_image(objectives[objective_id].name)

    if objectives[objective_id].requires != "none" and not items[objectives[objective_id].requires].visited:
        print("")
        print(color_object(objectives[objective_id].name) + " asks for a " +
              color_object(objectives[objective_id].requires) + ". Sadly you can't find it in your bag.")
    else:
        print("")
        print(color_object(objectives[objective_id].name) + " gives you following quest:")
        print("")
        display_quest(objective_id)

        print("")
        print(color_object(objectives[objective_id].name) + " asks you if you want to open this quest.")
        print("")
        if yesno():
            print("")
            print(objectives[objective_id].url)

        print("")
        print(color_object(objectives[objective_id].name) + " also offers you the solution.")
        print("Do you want to hear it?")
        print("")
        if yesno():
            print("")
            display_solution(objective_id)


# displays a colored ANSI image, depending on the terminal size, requires external program
def display_image(image_name):
    try:
        # f = open(gamedata + "/images/" + image_name + ".jpg","r")
        os.system("/bin/jp2a \"" + game_data + "/images/" + image_name + ".jpg\" --colors --fill --color-depth=8")
        # f.close()
        return True
    except IOError:
        print(f"Image file not found for {image_name}")
        return False


# displays a quest markdown page
def display_quest(md_name):
    quest = fetch_one_from_db(f'SELECT * FROM objective where objective_id = {md_name};')
    if quest is not None:
        md = Markdown(str(bytes(quest[3]), 'utf-8'))
        console.print(md)
    else:
        console.print("No quest entry found.")


# displays a solution markdown page
def display_solution(md_name):
    creator = fetch_one_from_db(f'SELECT * FROM creator where creator_name = \'{creator_name}\';')
    creator_id = creator[0]

    quest = fetch_one_from_db(f'SELECT * FROM solution where objective_id = {md_name} and creator_id = {creator_id};')
    if quest is not None:
        md = Markdown(str(bytes(quest[3]), 'utf-8'))
        console.print(md)
    else:
        console.print("No solution entry found.")


# open a connection to PostgresSQL DB and return the connection
def get_db_connection():
    try:
        conn = psycopg2.connect(user="kringle",
                                password="kringle",
                                host="kringle_database",
                                port="5432",
                                database="kringle")
        return conn
    except (Exception, Error):
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
        if location == 0:
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

    return counter_loaded


# queries the user to enter a command and triggers the matching function
def query_user():
    global cont
    print("")
    cmd = input(color_notice("I want to ------------>") + " ")
    print("")
    if cmd == "cheat":
        cheat()
    elif cmd == "cry" or cmd == "c":
        cry()
    elif cmd == "beam" or cmd == "b":
        beam()
    elif cmd == "exit" or cmd == "e":
        cont = 0
    elif cmd == "grab" or cmd == "g":
        grab()
    elif (cmd == "inspect") or cmd == "i":
        inspect()
    elif cmd == "look" or cmd == "l":
        look()
    elif cmd == "meditate" or cmd == "m":
        meditate()
    elif cmd == "recap" or cmd == "r":
        recap()
    elif cmd == "talk" or cmd == "t":
        talk()
    elif cmd == "phone" or cmd == "p":
        phone()
    elif cmd == "question" or cmd == "q":
        question()
    elif cmd == "walk" or cmd == "w":
        walk()
    else:
        lost()


# start of the main program
# -------------------------
# sets default for command auto-completion
set_default_complete()
readline.parse_and_bind("tab: complete")  # Linux
# readline.parse_and_bind ("bind ^I rl_complete") # Mac
readline.set_completer(auto_complete)

if __name__ == '__main__':
    # open the JSON data file and build all object dictionaries
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

    while cont == 1:
        query_user()
else:
    print(f"Cannot be run as module import: {__name__}")
