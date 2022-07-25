import sqlite3
from sqlite3 import Error
import csv
import pandas as pd

csv_file = './static/2021 AUG/AMK_scopus.csv'
#print(df.to_string())
db_file = './static/db/expert.db'

try:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
except Error as e:
    print(e)


def insertLectInfo(Name):
    Position = "Associate Professor"
    Email = "nazmee@usm.my"
    Telephone = "+604 653 4638"
    Fax = "+604 653 3335"
    Room = "713"
    Address = "School of Computer Sciences, Universiti Sains Malaysia, 11800 USM. Pulau Pinang"
    ResearchCluster = "Data To Knowledge"
    Interest = "Software Engineering (reuse, requirement engineering & software design pattern), Multimedia Information Retrieval, Computer Games, Graphics & Animations, Big Data Analytics & Data Mining, UX Design"
    Specialization = "Visual Computing & Analytics, Information Visualization, Multimedia & Animations, Software Engineering (Software reuse, Requirement Engineering etc)"
    Qualification = """B.Comp. Sc. (Hon.), M.Sc., PhD., USM """
    sql = """INSERT INTO expertInfo(Name, Position, Email, Telephone, Fax, Room, Address, ResearchCluster, Interest,
    Specialization, Qualification) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
    c.execute(sql, (Name, Position, Email, Telephone, Fax, Room, Address, ResearchCluster, Interest, Specialization, Qualification))
    conn.commit()


def insertPublication():
    Name = "Wan Mohd Nazmee Wan Zainon, Associate Professor Dr."
    search_name = "%" + Name + "%"
    find_lect_sql = "SELECT COUNT(*) FROM expertInfo WHERE Name LIKE ?"
    c.execute(find_lect_sql, [search_name])
    count = c.fetchone()[0]
    print(count)
    if count == 0:
        insertLectInfo(Name)
        print("Lecturer Record Inserted!")
    else:
        print("Lecturer Record Exists!")

    conn.close()


insertPublication()