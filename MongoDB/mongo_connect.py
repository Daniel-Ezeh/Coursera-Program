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


# Select the 'training' database
db = connection.training

# Select the 'python' collection
collection = db.python

#Creating a sample document
doc = {
    'lab':'Accessing mongodb using python',
    'Subject':'No SQL Databases'
}

# Inserting a sample document
print("Inserting a document into the \'python\' collection.")
db.collection.insert_one(doc)

# Querying for all documents in 'training' database and 'python' collection
docs = db.collection.find()

print("printing the documents in the collection.")
for doc in docs:
    print(doc)

connection.close()


