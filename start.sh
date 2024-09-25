#!/bin/bash

# Change the working directory to the one storing the file to avoid problems
cd ${0%/*}

# Stop the bot before launching a new one, or there will be problems polling the updates
./stop.sh

printf "\nLaunching the Bot..."

# Get the private data variables values
source ".private/data.txt"

cd bot
source venv/bin/activate
python3 bot.py $bot_userId $bot_apiToken &

printf "\n\n"
