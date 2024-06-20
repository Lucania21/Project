import sqlite3
import time

def install():
    con = sqlite3.connect("C:\\Users\\Tobe\\Judah project\\app\\data\\project.db")
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS Filesmanager(id INTEGER PRIMARY KEY, name TEXT, date REAL, user_id TEXT, filepath TEXT, active INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS summaries(id INTEGER PRIMARY KEY, file_id INTEGER, category TEXT, date REAL, filepath TEXT, active INTEGER, userid TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, passwordhash TEXT, active INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS Session(user_id INTEGER, session_id TEXT, sessionkey TEXT, active INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS Quizlet(id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER, name TEXT, date_created REAL, top_score INTEGER, num_questions INTEGER, type TEXT, active INTEGER, userid TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS Questions(id INTEGER PRIMARY KEY AUTOINCREMENT, Questiontxt TEXT, wrongoption TEXT, correctoption TEXT, Quizlet_id INTEGER)")
    except sqlite3.Error as e:
        print("Error creating tables:", e)
    finally:
        con.close()

def DBupload(table, attributes):
    try:
        con = sqlite3.connect("C:\\Users\\Tobe\\Judah project\\app\\data\\project.db")
        cur = con.cursor()
        
        # Prepare query
        placeholders = ', '.join(['?'] * len(attributes))
        query = f"INSERT INTO {table} VALUES ({placeholders})"
        
        # Execute query with attributes
        cur.execute(query, attributes)
        con.commit()
        return 0
    except Exception as init:
        print("Error in DBupload:", init)
        return 1
    finally:
        con.close()

def DBretrieve(table, column, ID=None):
    con = sqlite3.connect("C:\\Users\\Tobe\\Judah project\\app\\data\\project.db")
    cur = con.cursor()
    try:
        if not column:
            column = '*'
        else:
            column = ', '.join(column)

        query = f"SELECT {column} FROM {table}"
        if ID:
            if len(ID) == 2:
                query += f" WHERE {ID[0]} = ?"
                cur.execute(query, (ID[1],))
            else:
                conditions = ' AND '.join([f"{ID[i]} = ?" for i in range(0, len(ID), 2)])
                values = [ID[i+1] for i in range(0, len(ID), 2)]
                query += f" WHERE {conditions}"
                cur.execute(query, values)
        else:
            cur.execute(query)
        res = cur.fetchall()
        return res
    except sqlite3.Error as e:
        print("Error retrieving data:", e)
        return None
    finally:
        con.close()

def DBedit(table, changes, condition):
    try:
        con = sqlite3.connect("C:\\Users\\Tobe\\Judah project\\app\\data\\project.db")
        cur = con.cursor()
        query = f"UPDATE {table} SET "
        query += ', '.join([f"{key} = ?" for key in changes.keys()])
        query += f" WHERE {condition[0]} = ?"
        values = list(changes.values()) + [condition[1]]
        cur.execute(query, values)
        con.commit()
        return 0
    except sqlite3.Error as e:
        print("Error editing data:", e)
        return 1
    finally:
        con.close()
