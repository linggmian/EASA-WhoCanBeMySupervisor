import sqlite3
from sqlite3 import Error
import pandas as pd
from pathlib import Path


def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def query(conn):
    try:
        c = conn.cursor()
        query_sql = " SELECT DISTINCT * FROM PUBLICATION WHERE `Author Keywords` LIKE '%Deep learning%'"
        c.execute(query_sql)
        q = c.fetchall()
        for row in q:
            print(row)
    except Error as e:
        print(e)


def insert(conn):
    try:
        c = conn.cursor()
        insert_query = "INSERT INTO Inverted_Index(Term, PublicationID, AuthorKeyword) VALUES ('Deep Learning', 75, 'Yes');"
        c.execute(insert_query)
    except Error as e:
        print(e)


def main():
    db_file = './static/db/expert.db'
    sql_create_table = ('''
    CREATE TABLE IF NOT EXISTS expertInfo (
        LecturerID integer PRIMARY KEY,
        Name TEXT NOT NULL,
        'Position' TEXT,
        Email TEXT,
        Telephone TEXT,
        Fax TEXT,
        Room integer,
        Address TEXT,
        ResearchCluster TEXT,
        Interest TEXT,
        Specialization TEXT,
        Qualification TEXT,
        Image BLOB
    )''')
    conn = create_connection(db_file)
    if conn is not None:
        query(conn)
        #insert(conn)
        #create_table(conn, sql_create_table)
        #csv_data = pd.read_csv('./static/2021 AUG/ZZ_scopus.csv')
        #csv_data.to_sql('ZZ_scopus', conn, if_exists='append', index=False)
    else:
        print("Error! Cannot make connection to database.")
    conn = None


if __name__ == '__main__':
    main()





