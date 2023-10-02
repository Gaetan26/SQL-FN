"""
Package of classic SQL         |   Version          = 0.0.1
query utility functions        |   Created on       = Mon 2nd Oct 2023
*You can `C R U D`             |   Author           = Gaëtan SUENGE
          | | | |              |   E-mail           = gaetansg26@gmail.com
          | | | Delete         |   Lines of codes   = 193
          | | Update                -(no blank lines & comments)
          | Read               |   GitHub           = https://www.facebook.com    
          Create                    -(with documentation)
"""


import sqlite3
from os.path import exists


global DATABASE
global SHOW_SQL_REQUEST
SHOW_SQL_REQUEST = False


VERSION = [0,0,1]
FUNCTIONS = ['INSERT', 'SELECT', 'SELECT_ONE', 'UPDATE', 'DELETE', 'setDatabase', 'setShowSqlRequest', 'print_']


def setDatabase(path):
    global DATABASE
    if exists(path):
        DATABASE = path
        return True
    return False


def setShowSqlRequest(bool):
    global SHOW_SQL_REQUEST
    SHOW_SQL_REQUEST = bool


def print_(r):
    global SHOW_SQL_REQUEST
    if SHOW_SQL_REQUEST:
        print(r)
        return True
    return False


def DELETE(table:str, where=dict):
    connected = False
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        connected = True

        request = "DELETE FROM %s "%table
        where_ = "WHERE "
        index = 0
        for key in where.keys():
            if index < len(where.keys())-1:
                where_ += f'{key}{where[key]} AND '
            else:
                where_ += f'{key}{where[key]} '
            index += 1
        request += where_

        print_(request)
        cursor.execute(request)
        conn.commit()
        if cursor:
            return True
        return False
    
    except Exception as err:
        print('DB Error == %s'%err)
        if connected:
            conn.rollback()
    
    finally:
        if not connected:
            return False
        cursor.close()
        conn.close()


def UPDATE(table:str, array:dict, where):
    connected = False
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        connected = True
    
        request = "UPDATE %s "%table
        
        set_ = "SET "
        index = 0
        for key in array.keys():
            if index < len(array.keys())-1:
                set_ += f'{key}=\'{array[key]}\', '
            else:
                set_ += f'{key}=\'{array[key]}\' '
            index += 1
        request += set_
        
        where_ = "WHERE "
        index = 0
        for key in where.keys():
            if index < len(where.keys())-1:
                where_ += f'{key}{where[key]} AND '
            else:
                where_ += f'{key}{where[key]} '
            index += 1
        request += where_

        print_(request)
        cursor.execute(request)
        conn.commit()
        if cursor:
            return True
        return False

    except Exception as err:
        print('DB Error == %s'%err)
        if connected:
            conn.rollback()
    
    finally:
        if not connected:
            return False
        cursor.close()
        conn.close()


def SELECT_ONE(table:str, array:list|str, where=None, order_by=None):
    r = SELECT(table, array,where,order_by,limit="0,1")
    if type(r) == list:
        if len(r) == 1:
            return r[0]
    return r
    

def SELECT(table:str, array:list|str, where=None, order_by=None, limit=None):
    connected = False
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        connected = True

        request = "SELECT "
        index = 0
        for key in array:
            if index < len(array)-1:
                request += "%s,"%key
            else:
                request += "%s "%key
            index += 1

        request += "FROM %s "%table
        if where is not None:
            where_ = "WHERE "
            index = 0
            for key in where.keys():
                if index < len(where.keys())-1:
                    where_ += f'{key}{where[key]} AND '
                else:
                    where_ += f'{key}{where[key]} '
                index += 1
            request += where_

        if order_by is not None:
            request += "ORDER BY %s "%order_by

        if limit is not None:
            request += "LIMIT %s"%limit

        print_(request)
        cursor.execute(request)
        if cursor:
            return cursor.fetchall()
        return False

    except Exception as err:
        print('DB Error == %s'%err)
        if connected:
            conn.rollback()
    
    finally:
        if not connected:
            return False
        cursor.close()
        conn.close()


def INSERT(table:str, array:dict):
    connected = False
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        connected = True

        request = "INSERT INTO %s ("%table
        index = 0
        for key in array.keys():
            if index < len(array.keys())-1:
                request += "%s,"%key
            else:
                request += "%s) "%key
            index += 1
        
        request += "VALUES ("
        values = list()
        index = 0
        for key in array.keys():
            if index < len(array.keys())-1:
                request += "?,"
            else:
                request += "?)"
            values.append(array[key])
            index += 1
        
        print_(request)
        cursor.execute(request, values)
        conn.commit()
        if cursor:
            return True
        return False
    
    except Exception as err:
        print('DB Error == %s'%err)
        if connected:
            conn.rollback()
    
    finally:
        if not connected:
            return False
        cursor.close()
        conn.close()

