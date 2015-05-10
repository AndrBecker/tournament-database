
--- Tournament database ---
--- Project 2 of Udacity Nanodegree Full-Stack Webdeveloper ---

This project contains the scripts to generate and operate
a database for a swiss-style tournament.
The database registers players and their matches.

The project follows the specification of the final project
of the Udacity course "Intro to Relational databases".


-- Presumptions for the operation of the tournament database

The number of players must be even.


-- How to generate the tournament database

- Install postgresql if not installed yet.

- Open psql (postgresql shell) and login with the credentials
  of the "postgres"-user.

- As to create the tournament-database execute the
  'tournament.sql'-script in the psql shell with the command:

  \i <path_to_script>/tournament.sql

- You can check the result of the script execution by
  connecting to the database with the command:

  \c tournament

- The contents of the database can be inspected by
  typing in the command:

  \d 

- As a result of the script execution the database 2 tables
  'players' and 'matches' and a number of views and sequences
  should have been created.



-- How to operate the tournament database

Use the python functions in python script 'tournament.py' with
a python interpreter to operate the tournament database.

- The database access parameters in the script 'tournament.py' 
  in the 'psycopg2.connect'-command in function 'connect'
  have to be adapted to the local postgresql setup:

  psycopg2.connect(database="tournament",
                   user="postgres", password="<password>",
                   host="127.0.0.1", port="5432")

  The user and host-parameters might have to be adapted.
  The password of the user has to be instantiated.



-- How to test the tournament database

Run the test script 'tournament_test.py' with a python 
interpreter to check whether the tournament database is
put up correctly. This can be done by typing into the
console the command:

python tournament_test.py




