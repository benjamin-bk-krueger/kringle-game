FROM ubuntu

MAINTAINER Ben Krueger <sayhello@blk.pm> version: 0.1

RUN apt-get update
RUN apt-get install -y libncurses-dev flex libssl-dev libelf-dev bc bison
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y jp2a
RUN apt-get install -y whois git curl

RUN pip3 install rich

RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN npm install --global yarn
RUN yarn global add wetty

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /home/game
RUN mkdir /home/game/images
RUN mkdir /home/game/quests

COPY *.sh /home/game/
COPY *.py /home/game/
COPY *.json /home/game/
COPY images/* /home/game/images/
COPY quests/* /home/game/quests/
COPY *.md /home/game/
COPY LICENSE /home/game/

EXPOSE 3000

RUN useradd -s /home/game/game.sh -p $(mkpasswd --hash=SHA-512 game) game

CMD ["wetty","-p","3000"]  
