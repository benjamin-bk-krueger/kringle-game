#!/bin/sh
docker run -d -it benjaminkrueger/2022-kringlecon
docker run -p 127.0.0.1:3000:3000 -d -it benjaminkrueger/wetty
