CREATE DATABASE bokadjangodatabase;

CREATE USER bokadjangouser WITH PASSWORD 'Boka2019Database';

ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE bokadjangodatabase TO bokadjangouser;