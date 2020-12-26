#!/bin/bash

# Look for the pids of the bots executing now
pids=($(pgrep -f bot.py))

if [ -z $pids ]; then
    pids=(0)
else
    for i in "${pids[@]}"; do
        printf "\nBot.py PID: $i\n"
    done
fi

# For each pid
for i in "${pids[@]}"; do

	# If it's a valid pid
    if [ $i -gt 0 ]; then

        printf "\nKilling the bot..."

		# Send the Ctrl+C Signal to the process to kill it
        kill -INT $i
		
		# Wait 1 second and check if the process is dead
        while kill -0 $i >/dev/null 2>&1
        do
            sleep 1
        done

        printf "\n"
    fi

done
