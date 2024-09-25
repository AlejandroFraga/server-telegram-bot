#!/bin/bash

# Change the working directory to the one storing the file to avoid problems
cd ${0%/*}

# Some variables
launch_file="start.sh"
private_file=".private/data.txt"
welcome="Welcome to the installation of the server-telegram-bot. Press enter to start..."

# Welcome message
read -p "$welcome" -s -r REPLY; echo # Jump line

# [Optional] Install expect for Devs to update the server-telegram-bot files by automatic sftp download in launch
printf "\n[Optional] Installing expect...\n\n"
sudo apt-get install expect

# Check if we are inside the server-telegram-bot directory
if [ "${PWD##*/}" != "server-telegram-bot" ]; then

	# Install git to clone the repository
	printf "\nInstalling git...\n\n"
	sudo apt-get install git

	# Clone the repository
	printf "\nCloning the GitHub repository...\n\n"
	git clone https://github.com/AlejandroFraga/server-telegram-bot

	# Remove the install file outside the repository
	rm -- "$0"

	# Move inside the project directory
	cd server-telegram-bot
fi

# Install python3
printf "\nInstalling python3...\n\n"
sudo apt-get install python3

# Install python3 pip to manage packages
printf "\nInstalling python3 pip...\n\n"
sudo apt-get install python3-pip

# Prepare to install speedtest
printf "\nInstalling speedtest...\n\n"
sudo apt-get install curl
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest

# Install pip3 virtual env to manage libraries
printf "\nInstalling pip3 virtual env\n\n"
pip3 install virtualenv --break-system-packages
python3 -m venv bot/venv
source bot/venv/bin/activate

# Install python-telegram-bot, emoji, psutil, requests and job-queue packages
printf "\nInstalling pip packages...\n\n"
python3 -m pip install python-telegram-bot --upgrade
python3 -m pip install emoji --upgrade
python3 -m pip install psutil --upgrade
python3 -m pip install requests --upgrade
python3 -m pip install "python-telegram-bot[job-queue]" --upgrade

# Change permissions to only allow the owner to read, write and execute the server-telegram-bot files
printf "\nChanging permissions...\n\n"
chmod u+x -R *

# Creating and adding the default private data
printf "\nCreating the private data file...\n\n"
install -Dv /dev/null .private/data.txt
printf "# Bot private info\nbot_userId=\"bot_userId\"\nbot_apiToken=\"bot_apiToken\"\n" >> $private_file

# Set the user id to talk to the telegram-bot-server
read -p "Please insert the telegram user id which will talk to the telegram-bot-server: " -r REPLY; echo # Jump line
if [ -n "$REPLY" ]; then
	sed -i -e 's,bot_userId=".*",bot_userId="'"$REPLY"'",g' $private_file
fi

# Set the api token of the telegram-bot-server
read -p "Please insert the Telegram Bot API Token: " -r REPLY; echo # Jump line
if [ -n "$REPLY" ]; then
	sed -i -e 's,bot_apiToken=".*",bot_apiToken="'"$REPLY"'",g' $private_file
fi

printf "\nInstallation process ended\n\n"

read -p "Do you want to launch the bot? " -n 1 -r REPLY; echo # Jump line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    ./$launch_file
fi
