#!/bin/bash

# Change the working directory to the uninstall.sh directory to avoid problems
cd ${0%/*}

# Stop the bot before launching a new one, or there will be problems polling the updates
./stop_bot.sh

# [Optional] For Devs, update the server-telegram-bot files by automatic sftp download in launch
#./update_bot.sh

cd bot

userid="userid"
apitoken="apitoken"

printf "\nLaunching the Bot..."

python3 bot.py $userid $apitoken &

printf "\n\n"
