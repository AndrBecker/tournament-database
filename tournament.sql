-- Table definitions for the tournament project.
--
-- The tournament database with its schema is created
-- by executing this file in the psql console with command
-- '\i tournament.sql'


-- Creation of tournament database and connection to the database --

drop database if exists tournament;

create database tournament;

\c tournament


-- Creation of tables players and matches --

-- Create table players

create table players ( id serial not null,
				name varchar(64) not null,
				primary key (id));

-- Create table matches

create table matches (  id serial not null,
				winner int references players(id),
				loser int references players(id),
				primary key (id));



-- Creation of views --

-- Create view count_wins (counts the wins per player)

create view count_wins as
	select p.id, count(winner) as nr_wins
	from players p left outer join matches m on p.id = m.winner group by p.id;


-- Create view count_matches (counts the matches per player)

create view count_matches as
	select p.id, count(m.*) as nr_matches
	from players p left outer join matches m on p.id = m.winner or p.id = m.loser group by p.id;


-- Create view player_standings (selects players with number of wins and matches)

create view player_standings as
	select p.id as id, p.name as name, cw.nr_wins as wins, cm.nr_matches as matches
	from players p, count_wins cw, count_matches cm where p.id = cw.id and p.id = cm.id
	order by cw.nr_wins desc;



