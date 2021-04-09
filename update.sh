#!/bin/bash

# Change the working directory to the one storing the file to avoid problems
cd ${0%/*}

user="user"
server="server"
copy="copy"
paste="paste"
password="password"

printf "\nUpdating the bot...\n"

./check-connection.exp $user $server $password

if [ $? -eq 0 ]; then

    printf "\nDeleting the old files...\n\n"

    rm -rv $paste*

    ./download-files.exp $user $server $copy $paste $password

    printf "\nGiving the dowloaded files execution permission...\n\n"

    chmod -v u+x $paste*

else

	printf "\nCan't establish connection to update...\n\n"

fi
