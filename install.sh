#!/bin/bash

# Some variables
launch_file="launch_bot.sh"
update_file="update_bot.sh"
welcome="Welcome to the installation of the telegram-bot-server. Press enter to start..."

# Change the working directory to the install.sh directory to avoid problems
cd ${0%/*}

# Welcome message
read -p "$welcome" -s -r REPLY; echo # Jump line

# Install python3
printf "\nInstalling python3...\n\n"
sudo apt-get install python3

# Install python3 pip to manage packages
printf "\nInstalling python3 pip...\n\n"
sudo apt-get install python3-pip

# Install python-telegram-bot, psutil and emoji packages
printf "\nInstalling pip packages...\n\n"
pip3 install python-telegram-bot --upgrade
pip3 install psutil --upgrade
pip3 install emoji --upgrade

# Prepare to install speedtest
printf "\nInstalling speedtest...\n\n"
sudo apt-get install gnupg1 apt-transport-https dirmngr
export INSTALL_KEY=379CE192D401AB61
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $INSTALL_KEY
echo "deb https://ookla.bintray.com/debian generic main" | sudo tee  /etc/apt/sources.list.d/speedtest.list
sudo apt-get update

# [Optional] Other non-official binaries will conflict with Speedtest CLI
sudo apt-get remove speedtest-cli

# Install speedtest
sudo apt-get install speedtest

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

# Change permissions to only allow the owner to read, write and execute the server-telegram-bot files 
printf "\nChanging permissions...\n\n"
chmod u+x -R *

# Set the user id to talk to the telegram-bot-server
read -p "Please insert the telegram user id which will talk to the telegram-bot-server: " -r REPLY; echo # Jump line
if [ -n $REPLY ]; then
	sed -i -e 's,userid=".*",userid="'"$REPLY"'",g' $launch_file
fi

# Set the api token of the telegram-bot-server
read -p "Please insert the Telegram Bot API Token: " -r REPLY; echo # Jump line
if [ -n $REPLY ]; then
	sed -i -e 's,apitoken=".*",apitoken="'"$REPLY"'",g' $launch_file
fi

# [Optional] Activate the auto update option in the launch script
# Usefull for Dev who doesn't want to be copying by hand in every modification and relaunch of the bot
read -p "Do you want to enable the update when launching option for Devs? [Y/y] " -r REPLY; echo # Jump line
if [[ $REPLY =~ ^[Yy]$ ]]; then
	sed -i -e 's,#\.\/'"$update_file"',\.\/'"$update_file"',g' $launch_file

	read -p "Enter the username of the server to update: " -r REPLY; echo # Jump line
	if [ -n $REPLY ]; then
		sed -i -e 's,user=".*",user="'"$REPLY"'",g' $update_file
	fi

	read -p "Enter the direction (ip or url) of the server: " -r REPLY; echo # Jump line
	if [ -n $REPLY ]; then
		sed -i -e 's,server=".*",server="'"$REPLY"'",g' $update_file
	fi

	read -p "Enter the directory/file/s you want to copy from the server: " -r REPLY; echo # Jump line
	if [ -n $REPLY ]; then
		sed -i -e 's,copy=".*",copy="'"$REPLY"'",g' $update_file
	fi

	read -p "Enter the directory/file/s you want to paste to the server: " -r REPLY; echo # Jump line
	if [ -n $REPLY ]; then
		sed -i -e 's,paste=".*",paste="'"$REPLY"'",g' $update_file
	fi

	read -p "Enter the password of the user of the server: " -s -r REPLY; echo # Jump line
	if [ -n $REPLY ]; then
		sed -i -e 's,password=".*",password="'"$REPLY"'",g' $update_file
	fi
fi

# Make the first speedtest so we accept the policy and check that works
printf "\nMaking the first speedtest so we accept the policy and check that works...\n\n"
speedtest

read -p "Do you want to launch the bot? " -n 1 -r REPLY; echo # Jump line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    ./$launch_file
fi
