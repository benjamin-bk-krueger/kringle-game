import json
from Room import Room

def lost():
    print("You're feeling a little lost.")
    print("You could *cry* for help.")

def help():
    print("Following commands are available:")
    print("cry, help, quit")

f = open("data.json")
data = json.load(f)

for i in data["rooms"]:
    print(i["room_name"])

myroom = Room()
myroom.name = "Start"
print(myroom.name)

while True:
    cmd = input("> ")
    if (cmd == "help"):
        help()
    elif (cmd == "cry"):
        help()
    elif (cmd == "quit"):
        break
    else:
        lost()

f.close()