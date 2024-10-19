from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlite3 
import os

DATABASE_URI = 'sqlite:///bot/database/database.db'  

def initdb() -> scoped_session:
    engine = create_engine(DATABASE_URI, echo=True, connect_args={"check_same_thread": False})
    

    execute_sql_from_file(engine, 'bot/database/db_schemas.sql') 
    

    return scoped_session(sessionmaker(bind=engine, autoflush=False))

def execute_sql_from_file(engine, filepath):
    with open(filepath, 'r') as file:
        sql_script = file.read()
    

    sql_commands = sql_script.split(';') 

    with engine.connect() as connection:
        for command in sql_commands:
            command = command.strip()
            if command: 
                try:
                    connection.execute(command)
                except Exception as e:
                    print(f"Erreur d'exécution de la commande : {command}")
                    print(f"Erreur: {e}")

base = declarative_base()

session = initdb()
