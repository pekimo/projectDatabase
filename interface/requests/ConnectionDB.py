import MySQLdb

class ConnectionDataBase:
    localhost = "localhost"
    username = "root"
    password = "qweasdzxc"
    db = "DB"
    def __init__(self):
        pass
    def connect(self):
        return MySQLdb.connect(self.localhost, self.username, self.password, self.db, init_command='set names UTF8')
    
def funUpdate(query, params):
    try:
        connection = ConnectionDataBase()
        connection = connection.connect()
        connection.autocommit(False)
        with connection:
            cursor = connection.cursor()
            connection.begin()
            cursor.execute(query, params)
            connection.commit()
            cursor.close()
            id = cursor.lastrowid
        connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Database error in update query.")
    return id

def funQuery(query, params):
    try:
        connection = ConnectionDataBase()
        connection = connection.connect()
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
        connection.close()
    except MySQLdb.Error:
        raise MySQLdb.Error("Database error in usual query")
    return result

def exist(entity, identificator, value):
    if not len(funQuery('SELECT id FROM ' + entity + ' WHERE ' + identificator + ' = %s', (value, ))):
        raise Exception("No such element")
    return