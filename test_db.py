import mysql.connector

def db_connection():
    import mysql.connector
    connection = mysql.connector.connect(host='localhost',
                                         database='test',
                                         user='root',
                                         password='')
    cursor = connection.cursor()
    return cursor,connection