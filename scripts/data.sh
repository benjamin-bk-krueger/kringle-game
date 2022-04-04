#!/bin/sh
git clone https://github.com/benjamin-bk-krueger/2021-kringlecon.git
cd 2021-kringlecon
#zip -r 2021-kringlecon.zip data.json images quests
zip -r 2021-kringlecon.zip images quests
mv 2021-kringlecon.zip ../
cd ..
cp 2021-kringlecon.zip /var/www/html/kringle_gamedata/2021-kringlecon.zip
rm -rf 2021-kringlecon*

