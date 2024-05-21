from pymongo import MongoClient
user = 'root'
password = 'MTY5NjktZGFuaWVs'
host = 'localhost'
connecturl = f'mongodb://{user}:{password}@{host}:27017/?authSource=admin'

print("Connecting to mongodb Server")
connection = MongoClient(connecturl)

print("Getting list of databases")
dbs = connection.list_database_names()

for db in dbs:
    print(db)
print("Closing the connection to the mongodb server")

connection.close()


