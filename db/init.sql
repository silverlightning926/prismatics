\echo 'Creating Database: prismatics'
CREATE DATABASE prismatics;
\c prismatics

\echo '\nCreating Schema: prismatics.tba'
DROP SCHEMA public AUTHORIZATION CURRENT_USER;
CREATE SCHEMA tba AUTHORIZATION CURRENT_USER;

\echo '\nCreating Table: prismatics.table.teams'
\ir 'tba/teams.sql'

\echo '\nCreating Table: prismatics.table.events'
\ir 'tba/events.sql'

\echo '\nCreating Table: prismatics.table.matches'
\ir 'tba/matches.sql'

\echo '\nCreating Table: prismatics.table.rankings'
\ir 'tba/rankings.sql'

\echo '\nCreating Table: prismatics.table.alliances'
\ir 'tba/alliances.sql'
