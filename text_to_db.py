#800080import re
import mysql.connector as sqlc
import imp
import nltk

import MySQLdb
from flask import Flask, render_template

ls_lines = []
file_name = "sample_data.txt"				#-- The text file provided

fob = open (file_name, "r")					#-- Reading the file line by line to get the headings
for i in fob:
	ls_lines.append (i)

ls_lines = (ls_lines[0])					#-- The following lines are used to derive a list with the headings of the table
ls_lines = re.sub ("[^A-Za-z0-9,]+", '', ls_lines)
ls_lines = ls_lines.replace (',', ' ')
ls_lines = nltk.word_tokenize (ls_lines)

i = 0
while (i < len (ls_lines)):
	idx = 0
	if ('name' in ls_lines [i]):			#-- If the heading is "First Name", then a space has to seperate the 2 words
		idx = ls_lines[i].index ("name")
	elif ('Name' in ls_lines [i]):
		idx = ls_lines[i].index ("Name")
	ls_lines[i] = ls_lines [i][:idx] + ' ' + ls_lines [i][idx:]
	i += 1

i = 0
while (i < len (ls_lines)):
	if (ls_lines[i][0] == " "):								#-- Removing unwanted spaces in front of the heading name
		ls_lines[i] = ls_lines[i] [1 : len(ls_lines[i])]
	i += 1

#----

def db_create():
	mydb = sqlc.connect (
		host = "localhost",
		user = "san",
		passwd = "san123"
	)

	mycursor = mydb.cursor()

	db_name = "EMP"									#-- The Database name provided in 'EMP'. But if we wish to change the name, we can supply the Database name here
	command = str ("CREATE DATABASE " + db_name)

	try:
		mycursor.execute (command)

	except:
		print ("Database already exists... Please create a DB with a different name.")

	create_table(db_name)

#----

def create_table(db_name):				#-- This function creates the table in the EMP Database
	mydb = sqlc.connect (
		host = "localhost",
		user = "san",
		passwd = "san123",
		database = db_name
)

	table_name = "emp_details"
	cursor = mydb.cursor()

	command = "CREATE TABLE emp_details (" + ls_lines[0] + " int (20), `" + ls_lines[1] + "` VARCHAR (300), `" + ls_lines[2] + "` VARCHAR (300), " + ls_lines[3] + " VARCHAR (350), " + ls_lines[4] + " INT (20))"
											#-- Giving the parameters of heading names into the string to be executed
	try:
		cursor.execute (command)
		insert_into_table (db_name, table_name)

	except:
		insert_into_table (db_name, table_name)

#----

def insert_into_table (db_name, table_name):		#-- Function to write content into the Database
	mydb = sqlc.connect (
		host = "localhost",
		user = "san",
		passwd = "san123",
		database = db_name
)

	cursor = mydb.cursor()

	sql = "INSERT INTO " + table_name + "(" + ls_lines[0] + ", `" + ls_lines[1] + "`, `" + ls_lines[2] + "`, " + ls_lines[3] + ", " + ls_lines[4] + ") VALUES (%s, %s, %s, %s, %s)"

	lines = []
	file_name = "sample_data.txt"

	fob = open (file_name, "r")
	for i in fob:
		lines.append (i)

	lines.remove (lines[0])			#-- This line is removed because it contains only the heading names
	for i in lines:
		temp = i
		temp = re.sub ('[^A-Za-z0-9,]+', '', temp)		#-- Removing all unwanted characters
		temp = temp.replace (',', ' ')
		temp_ls = nltk.word_tokenize (temp)				#-- Tokenizing the string to derive words

		if (len (temp_ls) <= 1):
			continue
		else:
			i = 0
			while (i < len (temp_ls [1])):
				if (ord (temp_ls [1][i]) in range (65, 91)):
					temp_ls[1] = temp_ls[1] [i : len (temp_ls [1])]
					break
				i += 1

		val = tuple (temp_ls)
		print (val)
		cursor.execute (sql, val)

		mydb.commit()
		cursor.execute ("SELECT * FROM emp_details")
		result = cursor.fetchall()

	#flask_web_connection1()

#----

def drop_database():			#-- Deletes the Database in order to overwrite the data
	mydb = sqlc.connect (
		host = "localhost",
		user = "san",
		passwd = "san123",
)

	cursor = mydb.cursor()
	try:
		cursor.execute ("DROP DATABASE EMP")
	except:
		print ("EMP Database has to be created first. ")

	db_create()

#----

import time
def query():
	mydb = sqlc.connect(
		host="localhost",
		user="san",
		passwd="san123",
		database = "EMP"
)
	cursor = mydb.cursor()
	try:
		cursor.execute ("SELECT * FROM emp_details WHERE `First name` = 'Rohit';")
		time.sleep (1.0)

		print("-------------------------------------------\n")
		result = cursor.fetchall()
		for i in result:
			print (i)

	except:
		print ("Invalid command... Please check the SQL Syntax.")

	try:
		cursor.execute ("SELECT * FROM emp_details WHERE salary >= 45000;")
		time.sleep (1.0)

		print ("-------------------------------------------\n")
		result = cursor.fetchall()
		for i in result:
			print(i)

	except:
		print("Invalid command... Please check the SQL Syntax.")

#--

if __name__ == "__main__":
	drop_database()
	#app.run()




#	--------------------------------------------

