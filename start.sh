#!/bin/bash

# Change the working directory to the one storing the file to avoid problems
cd ${0%/*}

# Stop the bot before launching a new one, or there will be problems polling the updates
./stop.sh

# [Optional] For Devs, update the server-telegram-bot files by automatic sftp download in launch
#./update.sh

cd bot

userid="userid"
apitoken="apitoken"

printf "\nLaunching the Bot..."

python3 bot.py $userid $apitoken &

printf "\n\n"
