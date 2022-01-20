#!/bin/bash
set -e

#ON_ERROR_STOP=1 --username "ckan" <<-EOSQL
psql -v --username "ckan" <<-EOSQL
    CREATE ROLE datastore_ro NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD 'datastore';
    CREATE DATABASE datastore OWNER ckan ENCODING 'utf-8';
    GRANT ALL PRIVILEGES ON DATABASE datastore TO ckan;
    CREATE EXTENSION POSTGIS;
    ALTER VIEW geometry_columns OWNER TO ckan;
    ALTER TABLE spatial_ref_sys OWNER TO ckan;
EOSQL
