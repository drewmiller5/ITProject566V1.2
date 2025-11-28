#!/bin/bash

echo 'Creating logs directory if it does not already exist...'
mkdir -p logs
echo 'Deleting old log files if they exist...'
rm -f logs/*

# Date created
d=$(date)
echo $d

mysql < DB_Create_V3/Create_Insert.sql
echo $d 'Database Created'