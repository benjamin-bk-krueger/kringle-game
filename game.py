import os  # necessary to access terminal size and file operations
import readline  # necessary to be able to auto-complete user
import urllib.request  # necessary to download game data
import psycopg2  # necessary to connect to PostGreSQL database

from rich.console import Console  # necessary for markdown display
from rich.markdown import Markdown  # necessary for markdown display
from psycopg2 import Error  # necessary for DB error handling

from room import Room
from objective import Objective
from junction import Junction
from item import Item
from character import Character
from colors import Bcolors

# the app configuration is done via environmental variables
POSTGRES_HOST = os.environ['POSTGRES_HOST']  # DB connection data
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PW = os.environ['POSTGRES_PW']
POSTGRES_DB = os.environ['POSTGRES_DB']
S3_FOLDER = os.environ['S3_FOLDER']  # where S3 buckets are located
GAME_DATA = os.environ['HOME'] + "/.kringlecon"  # directory for game data
URL_PREFIX = S3_FOLDER + "/world/" + "DEMO_WORLD"  # S3 files for specific world

# game flow control
PROG_CONT = 1  # the program will run until this value is set to 0
PROG_LOC = 0  # the starting room, changes later in the game by walking around
PROG_LOGO = "logo"  # logo

# game data model
rooms = dict()  # contains all available rooms
objectives = dict()  # contains all available objectives
junctions = dict()  # contains all junctions between the rooms
items = dict()  # contains all available items
characters = dict()  # contains all available side characters

# game vocabulary options
vocabulary = []  # contains autocomplete values
default_actions = ['beam', 'cry', 'exit', 'grab', 'inspect', 'look', 'meditate', 'phone', 'question', 'recap', 'talk',
                   'walk']  # default actions

console = Console()  # markdown output to console


# --------------------------------------------------------------
# database functions
# --------------------------------------------------------------

# open a connection to PostgresSQL DB and return the connection
def get_db_connection():
    try:
        conn = psycopg2.connect(user=POSTGRES_USER,
                                password=POSTGRES_PW,
                                host=POSTGRES_HOST,
                                port=POSTGRES_PORT,
                                database=POSTGRES_DB)
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


# --------------------------------------------------------------
# Internal functions
# --------------------------------------------------------------

# loads game data from a Postgres DB into a data model
def load_data():
    global PROG_LOC
    global PROG_LOGO
    global URL_PREFIX

    counter_loaded = 0

    record = fetch_one_from_db("SELECT version();")
    print("Welcome to KringleGames.\n")

    counter = 0
    world_id = 0
    print("Please select a " + color_header("world"))
    all_worlds = fetch_all_from_db(f"select * from world order by world_id asc;")
    for world in all_worlds:
        counter = counter + 1
        print(f"|- [{world[0]}] {world[2]}")

    if counter > 0:
        print("")
        id_text = input(color_notice("I want to discover [id] ---->") + " ")
        try:
            world_id = int(id_text)
        except ValueError:
            world_id = 0
        set_default_complete()

    if world_id > 0:
        for world in all_worlds:
            if world[0] == world_id:
                URL_PREFIX = S3_FOLDER + "/world/" + world[2]
                PROG_LOGO = world[5]

        room_records = fetch_all_from_db(f"SELECT * FROM room WHERE world_id = {world_id} order by room_id asc;")
        for i in room_records:
            room = Room()
            room.name = i[2]
            room.description = i[3]
            room.img = i[4]
            rooms.update({i[0]: room})
            counter_loaded = counter_loaded + 1

            # the first room is the starting location
            if PROG_LOC == 0:
                PROG_LOC = i[0]

        item_records = fetch_all_from_db(f"select * from item WHERE world_id = {world_id} order by item_id asc;")
        for i in item_records:
            item = Item()
            item.name = i[3]
            item.description = i[4]
            item.location = i[1]
            items.update({i[0]: item})
            counter_loaded = counter_loaded + 1

        person_records = fetch_all_from_db(f"select * from person WHERE world_id = {world_id} order by person_id asc;")
        for i in person_records:
            character = Character()
            character.name = i[3]
            character.description = i[4]
            character.location = i[1]
            characters.update({i[0]: character})
            counter_loaded = counter_loaded + 1

        objective_records = fetch_all_from_db(f"select * from objective WHERE world_id = {world_id} order by objective_id asc;")
        for i in objective_records:
            objective = Objective()
            objective.name = i[3]
            objective.description = i[5]
            objective.img = i[10]
            objective.location = i[1]
            objective.difficulty = i[6]
            objective.url = i[7]
            objective.supportedby = i[8]
            objective.requires = i[9]
            objectives.update({i[0]: objective})
            counter_loaded = counter_loaded + 1

        junction_records = fetch_all_from_db(f"select * from junction WHERE world_id = {world_id} order by junction_id asc;")
        for i in junction_records:
            junction = Junction()
            junction.destination = i[3]
            junction.location = i[1]
            junction.description = i[4]
            junctions.update({i[0]: junction})
            counter_loaded = counter_loaded + 1

    return counter_loaded


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
    answer = input(color_notice("I am saying [y,yes] or [n,no] ---->") + " ")
    if answer == "yes" or answer == "y":
        return True
    else:
        return False


# talk to a character
def talk_to(objective_id):
    print("")
    print("You are talking to " + color_object(objectives[objective_id].name))
    display_image(objectives[objective_id].img)

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
        print(color_object(objectives[objective_id].name) + " says he might know people who have solved this quest.")
        all_solutions = fetch_all_from_db(f"select s.solution_id, c.creator_name, s.solution_text from solution s, objective o, world w, creator c where o.objective_id={objective_id} and s.visible = 1 and s.objective_id = o.objective_id and o.world_id = w.world_id and w.visible = 1 and s.creator_id = c.creator_id;")
        counter = 0
        for solution in all_solutions:
            counter = counter + 1
            print(f"|- [{solution[0]}] {solution[1]}")

        if counter > 0:
            print("")
            id_text = input(color_notice("I want to hear the solution from [id] ---->") + " ")
            try:
                solution_id = int(id_text)
            except ValueError:
                solution_id = 0
            if solution_id > 0:
                print("")
                display_solution(solution[2])
            else:
                print("")
                print("You decide you " + color_alert("don't want to hear that solution") + " right now.")
        else:
            print("")
            print("After a moment " + color_object(objectives[objective_id].name) + " mentions " + color_alert("no one has created a solution") + " yet.")
        set_default_complete()


# displays a colored ANSI image, depending on the terminal size, requires external program
def display_image(image_url):
    try:
        # shutil.rmtree(game_data)
        # os.mkdir(game_data)
        urllib.request.urlretrieve(URL_PREFIX + "/" + image_url, GAME_DATA + "/" + image_url)

        # f = open(game_data + "/images/" + image_name + ".jpg","r")
        # os.system("/bin/jp2a \"" + game_data + "/images/" + image_url + ".jpg\" --colors --fill --color-depth=8")
        # f.close()
        os.system("/bin/jp2a \"" + GAME_DATA + "/" + image_url + "\" --colors --fill --color-depth=8")

        return True
    except IOError:
        print(f"Image file not found for {image_url}")
        return False


# displays a quest markdown page
def display_quest(md_name):
    quest = fetch_one_from_db(f'SELECT * FROM objective where objective_id = {md_name};')
    if quest is not None:
        md = Markdown(str(bytes(quest[11]), 'utf-8'))
        console.print(md)
    else:
        console.print("No quest entry found.")


# displays a solution markdown page
def display_solution(solution):
    if solution is not None:
        md = Markdown(str(bytes(solution), 'utf-8'))
        console.print(md)
    else:
        console.print("No solution entry found.")


# --------------------------------------------------------------
# player action functions
# --------------------------------------------------------------

# only triggered once automatically when the player arrives (starts the program) - no command assigned
def arrive():
    display_image(PROG_LOGO)
    print("")
    print("You are arriving at a " + color_header("strange and unknown location") + ".")
    print("You are feeling a little dizzy.")
    print("What should be your " + color_ok("next steps") + "? You are pausing for a moment.")
    rooms[PROG_LOC].visited = True


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
        if objective.location == PROG_LOC and objective.difficulty > 0:
            print("In this room you can see " + color_object(objective.name) + ". " + objective.description)
            if objective.supportedby != "none":
                print("|- " + objective.supportedby + " can you give some hints for this quest.")
            if objective.visited:
                print("`- You " + color_ok("already have talked") + " to " + objective.name + " before.")
            else:
                print("`- You have " + color_alert("not talked") + " to " + objective.name + " yet.")
            print("")

    for item_id, item in items.items():
        if item.location == PROG_LOC:
            if not item.visited:
                print("In a corner you can see a " + color_object(item.name) + " lying around. " + item.description)
                print("")

    for character_id, character in characters.items():
        if character.location == PROG_LOC:
            print("Furthermore you can see " + color_object(character.name) + ". " + character.description)
            print("")

    for junction_id, junction in junctions.items():
        if junction.location == PROG_LOC:
            print(junction.description + " you can see a junction to " +
                  color_object(rooms[junction.destination].name) + ".")
            if rooms[junction.destination].visited:
                print("`- You " + color_ok("have visited") + " that location already.")
            else:
                print("`- You " + color_alert("have not seen") + " that location yet.")


# think about the main quest in the game, triggered automatically when the player arrives - "meditate" command assigned
def meditate():
    print("A quest to " + color_header("help Santa") + " has brought you to this place.")
    print("You think about how all those creatures here could aid you in your quest.")


# have a quick look at this place - "look" command assigned
def look():
    print("You are currently at " + color_object(rooms[PROG_LOC].name) + " and " + color_header("admiring") +
          " what your eyes can see...")
    print("")
    display_image(rooms[PROG_LOC].img)
    print("")
    print(rooms[PROG_LOC].description)


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
        id_text = input(color_notice("I want to talk to [id] ---->") + " ")
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
        if objective.location == PROG_LOC:
            counter = counter + 1
            print(f"|- [{objective_id}] {objective.name}")

    if counter > 0:
        print("")
        id_text = input(color_notice("I want to talk to [id] ---->") + " ")
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
    global PROG_LOC

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
        dest = input(color_notice("I want to go to [id] ---->") + " ")
        try:
            destination = int(dest)
        except ValueError:
            destination = 0
        if PROG_LOC != destination and destination in rooms:
            print("")
            print("You are " + color_ok("going to") + " " + rooms[destination].name)
            PROG_LOC = destination
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
    global PROG_LOC

    print("You " + color_header("look around") + " for other places to reach.")

    # assign all connected rooms to the auto-completion list
    counter = 0
    for junction_id, junction in junctions.items():
        if junction.location == PROG_LOC:
            counter = counter + 1
            print(f"|- [{junction.destination}] {rooms[junction.destination].name}")

    if counter > 0:
        print("")
        dest = input(color_notice("I want to go to [id] ---->") + " ")
        try:
            destination = int(dest)
        except ValueError:
            destination = 0
        if PROG_LOC != destination and destination in rooms:
            print("")
            print("You are " + color_ok("going to") + " " + rooms[destination].name)
            PROG_LOC = destination
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
        if item.location == PROG_LOC and item.visited is not True:
            counter = counter + 1
            print(f"|- [{item_id}] {item.name}")

    if counter > 0:
        print("")
        id_text = input(color_notice("I want to grab [id] ---->") + " ")
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
    print("You " + color_header("have visited") + " " + str(counter_r) + " room(s). You feel like there is/are " +
          str(len(rooms) - counter_r) + " more to discover.")
    print("You " + color_header("have talked") + " to " + str(counter_o) + " creature(s). You guess there is/are " +
          str(len(objectives) - counter_o) + " more waiting for contact.")
    print("You " + color_header("have grabbed") + " " + str(counter_i) + " item(s). Maybe you can put " +
          str(len(items) - counter_i) + " additional one(s) into your bag.")


# queries the user to enter a command and triggers the matching function
def query_user():
    global PROG_CONT
    print("")
    cmd = input(color_notice("I want to [command] ---->") + " ")
    print("")
    if cmd == "cheat":
        cheat()
    elif cmd == "cry" or cmd == "c":
        cry()
    elif cmd == "beam" or cmd == "b":
        beam()
    elif cmd == "exit" or cmd == "e":
        PROG_CONT = 0
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

    while PROG_CONT == 1:
        query_user()
else:
    print(f"Cannot be run as module import: {__name__}")
