#!/bin/bash

if [ ! -f "$1" ]
then
    curl "$1"
fi

if [ ! -f "$2" ]
then
    curl "$2"
fi

unzip "$1" -d "_old_zip/"
unzip "$2" -d "_new_zip/"

mkdir "_old/" "_new/"

cd "$1"
unbrotli system.new.dat.br
../sdat2img/sdat2img.py system.transfer.list system.new.dat
sudo mount -t ext4 -o loop system.img "../_old/"
cd -

cd "$2"
unbrotli system.new.dat.br
../sdat2img/sdat2img.py system.transfer.list system.new.dat
sudo mount -t ext4 -o loop system.img "../_new/"
cd -

cp -r "template/" "_result/"

./generate_delta.py "_old" "_new" "_result"

cd "_result/"
zip -qr0 "../delta.zip" .
cd -

sudo umount "_old/"
sudo umount "_new/"

rm -rf "_old_zip/" "_new_zip/" "_old/" "_new/" "_result/"