
--- Tournament database - Project 2 of Udacity Nanodegree Full-Stack Webdeveloper ---

This project contains the scripts to generate and operate a database for
swiss-style tournament. The database registers players and their matches.

The project follows the specification of the final project of the Udacity
course "Intro to Relational databases".


-- Presumptions for the operation of the tournament database

The number of players must be even.


-- How to generate the tournament database with the "tournament.sql" script

- Install postgresql if not installed yet.
- Open psql (postgresql shell) and login with "postgres"-user credentials.
- Create the database with command 'create database tournament'.
- Execute the 'tournament.sql'-script with the
    command '\i <path_to_script>/tournament.sql'.
- The database 'tournament' should be filled with
    2 tables 'players' and 'matches' and a number of views and sequences;
    check with command '\d';


-- How to operate the tournament database

Use the python functions in python script 'tournament.py' with a
python interpreter to operate the tournament database.

- Possibly in the script 'tournament.py' the
'psycopg2.connect' - command in function 'connect' has to be adapted
to the local postgresql setup to something like

    psycopg2.connect(database="tournament",
			user="postgres", password="<password>",
			host="127.0.0.1", port="5432")


-- How to test the tournament database

Run script 'tournament_test.py' with a python interpreter
to check whether the tournament database is put up correctly.




