import sqlite3

def get_db():
    return sqlite3.connect('db/library.db')

def get_report_data():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions")
    return cur.fetchall()
