FROM ubuntu

MAINTAINER Ben Krueger <sayhello@blk.pm> version: 0.1

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y jp2a
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install rich

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

CMD ["/home/game/game.sh"]  
