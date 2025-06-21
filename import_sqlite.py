import textwrap

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

script = generate_script(
    sqlite_path='/sqlite_path/import_grist.grist',
    pg_uri='postgres:password@localhost:5432/dbname',
    db_schema='test_schema'
)
print(script)