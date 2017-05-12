#!/usr/bin/env bash

usage() {
	echo "Usage: $0 [-a|-p]"
	echo "-a  Configure all (virtualenv and python packages)"
}

packages="python3 fluidsynth alsa-tools"

pip_packs="mido"
pip="pip3 install --user ${pip_packs}"

while getopts ":ap" o; do
    case "${o}" in
        a)
            packages=${packages} tightvncserver
            ;;
        p)
            echo Installing the following python packages
            echo ${pip_packs}
            ${pip}
            exit
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
${pip}

