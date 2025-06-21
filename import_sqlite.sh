#!/bin/bash

SQLITE_PATH="$1"
PG_URI="$2"
DB_SCHEMA="$3"
PGLOADER_SCRIPT_NAME="$4"

if [ -z "$SQLITE_PATH" ] || [ -z "$PG_URI" ] || [ -z "$DB_SCHEMA" ] || [ -z "$PGLOADER_SCRIPT_NAME" ]; then
    echo "SQLITE_PATH, PG_URI, DB_SCHEMA or PGLOADER_SCRIPT_NAME is empty"
    echo "Command: $0 <path-to-sqlite> <postgresql-uri> <db-schema> <pgloader-script-name>"
    exit 1
fi

echo "Generating $PGLOADER_SCRIPT_NAME.load file"
# Generate the load file
cat <<EOF > $PGLOADER_SCRIPT_NAME
LOAD DATABASE
     FROM sqlite:///$SQLITE_PATH
     INTO postgresql://$PG_URI
CAST type date TO date USING unix-timestamp-to-timestamptz
SET search_path TO '$DB_SCHEMA'
WITH include drop, create tables, create indexes, reset sequences
EXCLUDING TABLE NAMES LIKE '_grist%'
;
EOF

echo "Starting to import sqlite file to databse"

pgloader --verbose ./$PGLOADER_SCRIPT_NAME

echo "Import done"
