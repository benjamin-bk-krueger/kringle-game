#!/bin/sh
/usr/local/bin/docker-compose -f /home/benjamin2/docker-compose.yml down && /usr/local/bin/docker-compose -f /home/benjamin2/docker-compose.yml pull -q && /usr/local/bin/docker-compose -f /home/benjamin2/docker-compose.yml up -d
