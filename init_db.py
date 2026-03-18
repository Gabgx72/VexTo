import sqlite3
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database.db')
schema_path = os.path.join(basedir, 'schema.sql')

def init_db():
    connection = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_db()