#!/bin/bash

# Remove git
printf "\nUninstalling git...\n\n"
sudo apt-get remove git

# Remove speedtest
printf "\nUninstalling speedtest...\n\n"
sudo apt-get remove speedtest

# Remove python-telegram-bot, psutil and emoji packages
printf "\nUninstalling pip packages...\n\n"
pip3 uninstall python-telegram-bot
pip3 uninstall psutil
pip3 uninstall emoji

# Remove python pip
printf "\nUninstalling python3 pip...\n\n"
sudo apt-get remove python3-pip

# Remove python
printf "\nUninstalling python3...\n\n"
sudo apt-get remove python3

# Remove expect
printf "\nUninstalling expect...\n\n"
sudo apt-get remove expect

# Check if we are inside the server-telegram-bot directory
if [ "${PWD##*/}" == "server-telegram-bot" ]; then

	cd ../
else

	rm -- "$0"
fi

# Remove the repository
rm -rv server-telegram-bot
