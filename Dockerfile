FROM ubuntu:20.04

LABEL version="0.1"
LABEL maintaner="Ben Krueger <sayhello@blk.pm>"
#LABEL release-date="2020-04-05"
#LABEL promoted="true"

RUN apt-get update
RUN apt-get install -y python3 python3-pip jp2a whois
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y ssh

RUN pip3 install rich

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /home/game /home/game/images /home/game/quests

COPY *.sh *.py /home/game/
# COPY *.json /home/game/
# COPY images/* /home/game/images/
# COPY quests/* /home/game/quests/

RUN mkdir /run/sshd
RUN useradd -s /home/game/game.sh -p $(mkpasswd --hash=SHA-512 game) game

CMD ["/usr/sbin/sshd","-D"]
