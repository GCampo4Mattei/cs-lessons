import sqlite3 as sql

# database_script = 'schema.sql'
database_script = './assets/sql/schema.sql'

# database_name = 'myTeacher.db'
database_name = './assets/files/myTeacher.db'


def init_db():
    result = 1
    conn = sql.connect(database_name)
    print("Opened database successfully");

    # # Create
    # sqlTableTeacher = 'CREATE TABLE teacher (surname TEXT, name TEXT, classeconcorso TEXT)'
    # tablesToCreate = [sqlTableTeacher]
    # for currTable in tablesToCreate:
    #     conn.execute(currTable)
    #     print("Table created successfully");
    
    with open(database_script) as f:
        conn.executescript(f.read())
    
    # Initialize
    cur = conn.cursor()
    cur.execute("INSERT INTO teacher (cognome, nome, classeconcorso) VALUES (?,?,?)",("Rossi", "Giuseppe", "A012") )
    conn.commit()
    
    conn.close()
    result = 0
    return result

def get_db_connection():
    conn = sql.connect(database_name)
    conn.row_factory = sql.Row
    return conn