#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # Possibly need to adapt connection call to local setup
    #conn = psycopg2.connect(database="tournament", user="postgres", password="<password>", host="127.0.0.1", port="5432")
    #return conn;
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("truncate table matches;")
    conn.commit()
    conn.close()
    print "Table \'matches\' deleted"


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("truncate table players cascade;")
    conn.commit()
    conn.close()
    print "Table \'players\' deleted"


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("select count(*) from players;")
    nr_players = cur.fetchone()[0]
    conn.close()
    print "Nr players: " + str(nr_players)
    return nr_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into players (name) values (%s);", (name,))
    conn.commit()
    print "Player \'" + name + "\' registered successfully";
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("select id, name, wins, matches from player_standings;")
    rows = cur.fetchall()
    list = []
    for row in rows:
        #print "id = ", row[0]
        #print "name = ", row[1]
        #print "nr_winrs = ", row[2]
        #print "nr_matches = ", row[3], "\n"
        tup = ( row[0], row[1], row[2], row[3] )
        list.append (tup)
    conn.close()
    return list


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into matches (winner, loser) values (%s, %s);", (winner, loser))
    conn.commit()
    print "Match " + str(winner) + " - " + str(loser) + " reported successfully"
    conn.close()

 
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
    print "list: ", list

    if (len(list) % 2) != 0:
        print "Error: odd number of players !"
        return []

    pairingsList = [];
    for i in xrange(0,len(list)-1,2):
      tup1 = list[i]
      tup2 = list[i+1]
      pairingsList.append((tup1[0], tup1[1], tup2[0], tup2[1]))

    #print pairingsList
    return pairingsList

