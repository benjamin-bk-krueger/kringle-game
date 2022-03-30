FROM ubuntu:20.04

LABEL version="0.1"
LABEL maintaner="Ben Krueger <sayhello@blk8.de>"
#LABEL release-date="2020-04-05"
#LABEL promoted="true"

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-psycopg2 jp2a whois
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y ssh

RUN pip3 install rich

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /home/game/game.sh -p $(mkpasswd --hash=SHA-512 game) game
RUN mkdir /home/game/.kringlecon
RUN chown game /home/game/.kringlecon

COPY *.sh *.py /home/game/

RUN mkdir /run/sshd

CMD ["/usr/sbin/sshd","-D"]
