from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

def get_connection():

    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GBOLAHAN\\SQLEXPRESS;'
        'DATABASE=KNL_Barbers;'
        'Trusted_Connection=yes;'
    )

    return conn