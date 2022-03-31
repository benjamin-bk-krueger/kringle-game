#!/bin/sh
docker run -d -it benjaminkrueger/kringle-game
docker run -p 127.0.0.1:3000:3000 -d -it benjaminkrueger/wetty
docker run -d -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -p 127.0.0.1:5432:5432 -it postgres
