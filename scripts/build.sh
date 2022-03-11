#!/bin/sh
docker build -t benjaminkrueger/2022-kringlecon -f Dockerfile .
docker build -t benjaminkrueger/wetty -f wetty/Dockerfile .    
