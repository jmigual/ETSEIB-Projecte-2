#!/usr/bin/env bash

usage() {
	echo "Usage: $0 [-a|-p]"
	echo "-a  Configure all (virtualenv and python packages)"
}

all=false
while getopts ":a" o; do
    case "${0}" in 
        a)
            all=true
            ;;
        *)
            usage
            exit
            ;;
    esac
done

if [ ${all} = true ]; then
    echo Installing fluidsynth
    sudo apt install python3 fluidsynth jackd alsa-tools alsa-util -y

    echo Installing virtual environment
    pip3 install virtualenv
    virtualenv ./virtualenv
fi

source virtualenv/bin/activate

echo ========================================================
echo To finish the virtualenv installation you need to execute
echo source bin/activate
echo ========================================================
