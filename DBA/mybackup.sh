#!/bin/sh

# Set the folder where the database backup will be stored
backupfolder=/home/project/backups


sqlfile=$backupfolder/all-databases-backup.sql

# Create a backup

if mysqldump --all-databases --user=root --password=MzAwNDctZGFuaWVs  > $sqlfile ; then
   echo 'Sql dump created'
else
   echo 'pg_dump return non-zero code No backup was created!' 
   exit
fi

current_date=$(date +%Y%m%d)
dest_path=/home/project/mysqldumps/$current_date/

if [ -d "/home/project/mysqldumps/" ]; then
    echo "Folder exists"
else
    mkdir /home/project/mysqldumps/
    echo "Folder created"
fi


if [ -d "$dest_path" ]; then
    echo "Folder exists"
else
    mkdir $dest_path
    echo "Folder \'$dest_path\' created"
fi


cp $sqlfile $dest_path

rm $sqlfile
echo "Removed from the old file."