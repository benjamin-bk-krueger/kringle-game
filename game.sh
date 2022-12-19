#!/bin/sh
chmod 0750 /home/game/.profile
. /home/game/.profile
cd /home/game/ && python3 game.py
