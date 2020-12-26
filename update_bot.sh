#!/bin/bash

user="user"
server="server"
copy="copy"
paste="paste"
password="password"

printf "\nUpdating the bot...\n"

./check_connection.exp $user $server $paste $password

if [ $? -eq 0 ]; then

    printf "\nDeleting the old files...\n\n"

    rm -rv $paste*

    ./download_files.exp $user $server $copy $paste $password

    printf "\nGiving the dowloaded files execution permission...\n\n"

    chmod -v u+x $paste*

else

	printf "\nCan't establish connection to update...\n\n"

fi
