#!/usr/bin/env bash

usage() {
	echo "Usage: $0 [-a|-p]"
	echo "-a  Configure all (virtualenv and python packages)"
}

all=false
while getopts ":a" o; do
    case "${o}" in
        a)
            all=true
            ;;
        *)
            echo "Unknown option: ${OPTARG}"
            usage
            exit
            ;;
    esac
done

if ${all}; then
    echo Installing fluidsynth and necessary tools
    sudo apt install python3 fluidsynth tightvncserver alsa-tools -y
fi

