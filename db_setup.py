from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# from flask_mysqldb import MySQL
from flask import Flask
import mysql.connector
def create_connection():
    uri = "mongodb+srv://sfa:skill@cluster0.go6mb5d.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

def flask_app_creation():
    app = Flask(__name__)
    return app
# def create_connection_sql():
#     print("working on creating client")
#     connection = mysql.connector.connect(host='localhost',
#                                          database='test',
#                                          user='root',
#                                          password='')
#
#
#     return connection


def create_db(client):
    user_db = client.RumenoDb
    rumeno_client = user_db.RumenoCollection
    print("created collection successfully")
    return rumeno_client

def insert_method(conn,data_dict):
    conn.insert_one(data_dict)
    return "success"

def search_method(conn,data_dict):
     conn.find(data_dict)
     return "yes"


if __name__ == "__main__":
    app = flask_app_creation()
    create_connection_sql(app)
    # client = create_connection()
    # conn = create_db(client)
    # res = insert_method(conn)
    # print(res)