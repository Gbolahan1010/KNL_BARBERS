import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Psalm23:1-3",
        database="KNL_BARBERS"
    )