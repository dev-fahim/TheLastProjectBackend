CREATE DATABASE bokadjangodatabase;

CREATE USER bokadjangouser WITH PASSWORD 'Boka2019Database';

ALTER ROLE bokadjangouser SET client_encoding TO 'utf8';
ALTER ROLE bokadjangouser SET default_transaction_isolation TO 'read committed';
ALTER ROLE bokadjangouser SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE bokadjangodatabase TO bokadjangouser;