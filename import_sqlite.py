import textwrap
import configparser


def generate_script(sqlite_path: str, pg_uri: str, db_schema: str) -> str:
    return textwrap.dedent(f"""
        LOAD DATABASE
            FROM sqlite:///{sqlite_path}
            INTO postgresql://{pg_uri}
        CAST type date TO date USING unix-timestamp-to-timestamptz
        SET search_path TO '{db_schema}'
        WITH include drop, create tables, create indexes, reset sequences
        EXCLUDING TABLE NAMES LIKE '_grist%'
        ;
    """)


config = configparser.ConfigParser()
config.read('config.ini')

script = generate_script(
    sqlite_path=config['sqlite']['sqlite_path'],
    pg_uri=config['database']['db_uri'],
    db_schema=config['database']['schema']
)
print(script)

# Create script file on file system
PGLOADER_SCRIPT_NAME = 'grist.load'
with open(PGLOADER_SCRIPT_NAME, 'w') as f:
    f.write(script)

# Run pgloader command
import subprocess
subprocess.run(['pgloader', '--verbose', PGLOADER_SCRIPT_NAME])


# Remove script from file system
import os
os.remove(PGLOADER_SCRIPT_NAME)
