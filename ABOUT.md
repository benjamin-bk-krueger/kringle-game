***2022-02-14***

Today I took the decision I want to (re-)gain developer's skills (sadly my job is rather "managerial"). There are so many interesting technologies and tools out there you should know more about. So my plan is to build a project using all those technologies and tools and to learn at the same time. I don't know how much time I can invest here but to see my own progress I'm writing these notes at the same time.  
My theme will be the SANS Holiday Hack Challenge (https://www.sans.org/mlp/holiday-hack-challenge/). My goal is to create some console-based adventure game like the gold old LucasArts games in the 90s. It should mimic the original game and offer a walkthrough for the original game's quests at the same time. 

I have set up a GitHub Repository to hold all my project files. I have cloned that repository both on my MacBook as well as on my Mac Mini. Currently it's just a way to keep these directories in sync but I guess I'll get in touch with more advanced features in the future.

Python seems to be the ideal language, it's well known, robust, easy to learn and has a lot of libraries. I have learned Java programming 15 years ago but I guess that knowledge is almost useless. I have build some bash scripts to automate things but that's all for now.

The original game allows the player to walk around, enter different rooms and solve challenges and get hints. I'll start by creating a room object (at least that's something I can remember - object oriented programming is a good thing I guess).

Btw. I'm writing this log in markdown, so I'm starting with three technologies on my I-want-to-learn-tech-stack: Python, Markdown, GIT

***2022-02-14 (late evening)***

Wow, that's fun. I'm feeling like "I can't stop, just another feature to be implemented". Rooms do have attributes (ID, name, description). Guess it's a good thing to keep that separate.   Maybe the program will support completely different scenarios/worlds just be providing other game data. 

JSON seems to be a good format to provide this kind of game data. Python allows me to load data from a JSON file using just 2 or 3 lines of code.

***2022-02-15***

The player should have to ability to enter commands like in the good old command line adventures. Currently I'm limited to look and inspect a room.

To make my game more enjoyable I want the rooms to be displayed somehow. Playing around with some online JPEG to ASCII converters. I'll take the original game pictures and create an ASCII art version.

Just realized a user might have different terminal sized (standard is 80 characters width). I'll create ASCII art for 80 and 160 characters width and let Python decide what's the best option.

Added a second object: "objective". Objectives are the challenges a player needs to solve. Each room can contain objectives. Need to link both rooms and objectives.

The user is now able to look at a room and to talk with an objective's owner. Feels really interactive.

***2022-02-16***

Entering commands completely might be tedious. Python offers another library (readline) which allows you to auto-complete commands by pressing TAB. I'm realizing how powerful Python can be.

Just one room and one objective is nice. Introducing a third object: "junction". This allows me to connect rooms and the player to "walk" around.

Added some shortcuts for the player: "phone" means talk to an objective's owner anywhere, "beam" means travelling to a place from anywhere

***2022-02-17***

The code got quite messy already. I'm tidying up some parts to re-use functions ... ok ... another thing I remembered from my Java courses.

Each cool game or program should have a logo ... implementing one using ASCII art.

In the original game each objective has a challenge the player needs to solve. My game sould be able to display the challenge along with the solution. I'm using yet another Python library (rich) to display Markdown on the console. Each objective has a Markdown file containing the challenge and one for the solution. Talking to an objective's owner displays both files.

***2022-02-18***

Added the fourth technology to my I-want-to-learn-tech-stack: Docker!  
I have created a very simple Dockerfile taking an Ubuntu image, adding Python and the modules as well as my program files to it.  
Created some bash scripts to automate things: building a Docker container, running it, ...
Tested my shiny Docker container both on MacOS and Linux

***2022-02-19***

I don't feel confident creating all the ASCII images using a web tool anymore. Seems to be a lot of work and includes a lot of manual steps. There is a tool called JP2A which is able to read JPEG files and render ASCII art. There is no real Python implementation but I guess it's okay to rely on that external tool. Adding it to the Docker container is very simple. This way it doesn't matter if the user has the tool installed or not.  
Python is powerful, Docker is powerful, I'm feeling powerful!

I have a lot of ideas: multi lingual support, cloud (kubernetes?), better integration to the original game's challenges, error handling, ...  
Just set up a GitHub projects site to keep track of my tasks and ideas

A week is over and I feel like I really have achieved something. I have a small basic interactive game which supports configurable game data and can be launched anywhere using containerization. 

I don't know if I can keep this pace but instead of watching stupid serials on TV I'll want to invest at least a few hours each week to continue this journey. Let's see where it will end ...

***2022-02-19 (late evening)***

I got a working Docker container but for someone without a Docker installation the program cannot be used. It can be installed on a server and be accessed via SSH but maybe it's easier just to access the game using a web browser. The original game is using WeTTY. Why not use that one as well? Having some difficulties building WeTTY from sources but at the end I was successful. Modified the Docker container so WeTTY gets started when the container is running. Writing encryption (HTTPS, reverse proxy) on my todo list...

Started writing unit test cases...

Managed to trigger automatic code builds via GitHub Actions. My action is taking the code, building a Docker image and deploying it do Docker Hub at the end. No need to build anything locally anymore. 

Now I do have a really cool code pipeline. I can edit the code - as soon as I commit the changes to the GitHub repo I'll get a Docker image a few minutes afterwards in my Docker repository. A next step may be to deploy that image on some server, maybe some AWS service and host the container there. Enough infrastructure stuff for the moment. Guess I'll focus on the game itself again. 

WEEKEND TIME!!!

***2022-02-20***

Quickly ran the Docker container on a small AWS EC2 instance. Proof of Concept: Successful!!
Bought a book covering Python...  
Next week I'll join a bootcamp "GitHub for Everyone" hosted by INE. I'm sure I'll learn a lot of things.  
Guess setting up something like Kubernetes won't be so easy ... INE also has a lot of courses covering that 

***2022-02-22***

Added items as new object and feature to the game.  
Did a lot of rework to make the code much more readable and beautiful.  
Maybe I should read my Pyhon book before writing too much code ... the more code there is the more rework there may be ...

***2022-02-23***

Quickly implemented non-interactive side characters/objects and a cheat function.
Yeah, cheating, cheating :)

***2022-03-02***

I have attended a three days bootcamp hosted by INE: "GitHub for Everyone".  
Now I do know a lot more about issues, branches, pull request and actions.  
Always remember: Never ever commit to main!! ;-) 

***2022-03-12***

What a busy week...  
I realize having both WeTTY as well as the game in one repository and one Dockerfile is not a good idea. Even a small change in some Python file will trigger everything to be rebuilt.  
I have created a separate repository just for WeTTY.  Now I do have a WeTTY container and a game container. How can I connect those???
Searching the internet I have found docker-compose might be the solution.  
I have created a container stack using a docker-compose.yml file. It will start one container for WeTTY and one for the game which can be accessed by WeTTY via SSH. Really cool. This might be helpful later when I have the time to "learn" Kubernetes.

***2022-03-15***

Didn't manage to get minikube running on a VPS. Instead I have set up a VPS running an Apache web server. This one acts as a proxy and sends the requests to the WeTTY container.

***2022-03-15 (evening)***

Modified the Github Action so it will deploy the images to the VPS and run the docker containers automatically.

***2022-03-24***

Providing static game data (images, quests) might not be the best idea. So I put all that files into a ZIP file located in another public repository. The game is now able to fetch that file and parse the extracted files.  
This way providing updated game data or another completely different scenario is possible without re-deploying the application.
