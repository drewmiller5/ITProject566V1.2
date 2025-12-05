#!/bin/bash

# create logs directory if not there
echo 'Creating logs directory if it does not already exist...'
mkdir -p logs
echo 'Deleting old log files if they exist...'
rm -f logs/*

d=$(date)
echo $d

# Create Database Version 1
echo "Running Database Scriptss..."
echo  $d': Dropping database...' | tee -a logs/delete_database.log
mysql < Database/DB_Delete/Delete_Database.SQL 2>&1 | tee -a logs/delete_database.log
echo $d': Dropping user...' | tee -a logs/delete_user.log
mysql < Database/DB_Delete/Delete_User.SQL 2>&1 | tee -a logs/delete_user.log
echo $d': Creating database...' | tee -a logs/create_database.log
mysql < Database/DB_Create_V1/Create_Database.SQL 2>&1 | tee -a logs/create_database.log
echo $d': Creating user...' | tee -a logs/create_user.log
mysql < Database/DB_Create_V1/Create_User.SQL 2>&1 | tee -a logs/create_user.log
echo $d': Creating tables...' | tee -a logs/create_tables.log
mysql < Database/DB_Create_V1/Create_Tables.sql 2>&1 | tee -a logs/create_tables.log
echo $d': Inserting test data...' | tee -a logs/insert_test_data.log
mysql < Database/DB_Create_V1/Create_Data.sql 2>&1 | tee -a logs/insert_test_data.log