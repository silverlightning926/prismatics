\echo 'Creating Database: prismatics'
CREATE DATABASE prismatics;
\c prismatics

\echo '\nCreating Table: prismatics.public.etag'
\ir 'public/etags.sql'

\echo '\nCreating Schema: prismatics.tba'
CREATE SCHEMA tba AUTHORIZATION CURRENT_USER;

\echo '\nCreating Table: prismatics.tba.teams'
\ir 'tba/teams.sql'

\echo '\nCreating Table: prismatics.tba.events'
\ir 'tba/events.sql'

\echo '\nCreating Table: prismatics.tba.matches'
\ir 'tba/matches.sql'

\echo '\nCreating Table: prismatics.tba.rankings'
\ir 'tba/rankings.sql'

\echo '\nCreating Table: prismatics.tba.alliances'
\ir 'tba/alliances.sql'
