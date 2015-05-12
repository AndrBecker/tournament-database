#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
# For database access adapt the access parameters in the call of
# function 'psycopg2.connect' (user, password, host, port) in
# function 'connect' to the local setup.

# Import of required python modules.

import psycopg2


# Establishes a connection to postgresql database 'tournament'
# and returns the connection together with a cursor on the connection.
# The database access parameters might have to be edited for
# adaptation to the local setup (see notice above).

def connect():
    try:
        db = psycopg2.connect(database="tournament",
                              user="postgres", password="<password>",
                              host="127.0.0.1", port="5432")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error: no connection to the database")


# Deletes all entries in database table 'matches' without
# doing a table scan.

def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query = "TRUNCATE TABLE matches;"
    cursor.execute(query)
    db.commit()
    db.close()


# Deletes all entries in the tables 'matches' and 'players'.
# Entries in table 'matches' depend on entries in table
# 'players' by foreign key references so that the entries
# in table 'matches' have to be deleted before the entries
# in table 'players' they refer to are deleted. This order
# of deletion of dependent data is ensured by using the
# keyword 'CASCADE'.

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "TRUNCATE TABLE players CASCADE;"
    cursor.execute(query)
    db.commit()
    db.close()


# Returns the number of data records in table 'players' by
# aggregating all entries with the count function.

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT count(*) FROM players;"
    cursor.execute(query)
    nr_players = cursor.fetchone()[0]
    db.close()
    return nr_players


# Inserts a new data record in table 'players'. The unique serial
# id (primary key) is generated automatically by a sequence
# in the database.

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    param = (name,)
    cursor.execute(query, param)
    db.commit()
    db.close()


# Returns a list containing for each player a tuple made up of the
# player's id, name, number of wins and number of matches (= wins or
# losses). The function executes the database view 'player_standings'
# in the database and copies a tuple for each resulting data
# record into the result list.

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    query = "SELECT id, name, wins, matches FROM player_standings;"
    cursor.execute(query)
    rows = cursor.fetchall()
    list = []
    for row in rows:
        tup = (row[0], row[1], row[2], row[3])
        list.append(tup)
    db.close()
    return list


# Inserts a new data record into the table 'matches'.
# The parameters 'winner' and 'loser' must be set to
# ids of players registered in table 'players'.

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    params = (winner, loser)
    cursor.execute(query, params)
    db.commit()
    db.close()


# Returns a list of tuples each representing a pair of players which
# according to their player standing should play against each other in
# the next round in a swiss-style tournament. This is done by
# coupling players in the list returned by function 'playerStandings'.
# Each player in an even position in the list (beginning with position 0)
# is coupled with the following player in an uneven position in the list.
# An empty list is returned and an error message printed on the console
# in case there is an odd number of players in the tournament.

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    list = playerStandings()

    if (len(list) % 2) != 0:
        print "Error: odd number of players !"
        return []

    pairingsList = []
    for i in xrange(0, len(list)-1, 2):
        tup1 = list[i]
        tup2 = list[i+1]
        pairingsList.append((tup1[0], tup1[1], tup2[0], tup2[1]))

    return pairingsList
