# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 12:17:22 2020

@author: andmra2
"""

import sqlite3
from sqlite3 import Error

 
def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    dbFile = '//corp.hidria.com/aet/SI-TO-Izmenjava/Andrej_Mrak/ProgramData/AFM/users/usersSettings.db'
    try:
        conn = sqlite3.connect(dbFile)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn
 
#def create_connection(db_file):
#    """ create a database connection to the SQLite database
#        specified by db_file
#    :param db_file: database file
#    :return: Connection object or None
#    """
#    conn = None
#    try:
#        conn = sqlite3.connect(db_file)
#    except Error as e:
#        print(e)
# 
#    return conn




def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

 
 
def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid
 
 
def create_user(conn, user):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO UserAuth(username,status,hash1,hash2,hash3,hash4,hash5,hash6,hash7,hash8,hash9,hash10)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM UserAuth")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def select_username(conn, username):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()        
    cur.execute('SELECT * FROM UserAuth WHERE username LIKE "%s%%";' % username)
    
    rows = cur.fetchall()
    
    for row in rows:
        print(row)



 
 
def main():
    #database = r"C:\sqlite\db\pythonsqlite.db"
    sql_create_UserAuth_table = """CREATE TABLE IF NOT EXISTS UserAuth (
                                    username text NOT NULL,
                                    status text NOT NULL,
                                    hash1 text NOT NULL,
                                    hash2 text NOT NULL,
                                    hash3 text NOT NULL,
                                    hash4 text NOT NULL,
                                    hash5 text NOT NULL,
                                    hash6 text NOT NULL,
                                    hash7 text NOT NULL,
                                    hash8 text NOT NULL,
                                    hash9 text NOT NULL,
                                    hash10 text NOT NULL
                                );"""
    # create a database connection
    conn = create_connection()
    #create_table(conn, sql_create_UserAuth_table)
    with conn:
#        # create a new project
#        project = ('UserAuth');
#        project_id = create_project(conn, project)
 
        # tasks
        task_1 = ('Kr en', 'admin', 'gshfi', 'gshfi', 'gshfi', 'gshfi', 'gshfi', 'gshfi', 'gshfi', 'gshfi', 'gshfi', 'gshfi')
        #task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
 
        # create tasks
        #create_user(conn, task_1)
        #create_task(conn, task_2)
        #select_username(conn, 'Andrej Mrak')
        select_all_tasks(conn)
        
 
if __name__ == '__main__':
    main()

 

