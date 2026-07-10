import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="knl_user",
        password="@Kidlogan1010",
        database="KNL_BARBERS"
    )