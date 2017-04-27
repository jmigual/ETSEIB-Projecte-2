#!/usr/bin/env bash

usage() {
	echo "Usage: $0 [-a|-p]"
	echo "-a  Configure all (virtualenv and python packages)"
}

packages="python3 fluidsynth alsa-tools"

while getopts ":a" o; do
    case "${o}" in
        a)
            packages=${packages} tightvncserver
            ;;
        *)
            echo "Unknown option: ${OPTARG}"
            usage
            exit
            ;;
    esac
done

echo Installing fluidsynth and necessary tools
sudo apt install ${packages} -y

