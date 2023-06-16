FROM ubuntu:kinetic

LABEL version="0.9"
LABEL maintaner="Ben Krueger <sayhello@blk8.de>"

RUN apt-get update
RUN apt-get install -y python3 python3-pip python3-psycopg2 jp2a whois

RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y ssh

RUN pip3 install rich

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /run/sshd
RUN sed -i "s/session    optional     pam_motd.so  motd=\/run\/motd.dynamic/#session    optional     pam_motd.so  motd=\/run\/motd.dynamic/g" /etc/pam.d/sshd
RUN sed -i "s/session    optional     pam_motd.so noupdate/#session    optional     pam_motd.so noupdate/g" /etc/pam.d/sshd
RUN sed -i "s/#PrintLastLog yes/PrintLastLog no/g" /etc/ssh/sshd_config

RUN useradd -m -s /home/game/game.sh -p $(mkpasswd --hash=SHA-512 game) game

USER game

RUN mkdir /home/game/.kringlecon

COPY *.sh *.py /home/game/

USER root

CMD ["/usr/sbin/sshd","-D"]
