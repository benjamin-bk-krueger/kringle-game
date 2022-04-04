FROM ubuntu:20.04

LABEL version="0.9"
LABEL maintaner="Ben Krueger <sayhello@blk8.de>"

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-psycopg2 jp2a whois
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y ssh

RUN pip3 install rich

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /run/sshd

RUN useradd -m -s /home/game/game.sh -p $(mkpasswd --hash=SHA-512 game) game

USER game

RUN mkdir /home/game/.kringlecon

COPY *.sh *.py /home/game/

USER root

CMD ["/usr/sbin/sshd","-D"]
