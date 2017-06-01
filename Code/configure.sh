#!/usr/bin/env bash

usage() {
	echo "Usage: $0 [-p]"
	echo "Configure the device to work as director or player"
	echo "-p  Configure python packages only"
}

packages="python3 fluidsynth alsa-utils"

pip_packs="mido python-telegram-bot"
pip="pip3 install --user ${pip_packs}"

while getopts ":ap" o; do
    case "${o}" in
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

