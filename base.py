import sys
import mysql.connector

def create_conn(db_name):
    try:
        connection_db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Etydghcb6983",
                database=db_name
        )
    except mysql.connection.Error as db_connection_error:
        print(db_connection_error)
    return connection_db

def create_db(cursor_db, name_db):
    try:
        create_db_query = ("CREATE DATABASE " + name_db + ";")
        print(create_db_query)
        cursor_db.execute(create_db_query)
    except mysql.connection.Error as e:
        print(e)
    return

def create_table(cursor_db, connection_db, table):
    cursor_db.execute(table)
    connection_db.commit()
    return


def ins_table(cursor_db, connection_db, line):
    cursor_db.execute(line)
    connection_db.commit()
    return
