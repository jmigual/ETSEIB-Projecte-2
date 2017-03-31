#!/usr/bin/env bash

# Custom script to install all the dependencies to a raspberry
sudo apt install git -y
git clone https://github.com/jmigual/projecte2
./projecte2/Code/configure.sh -a