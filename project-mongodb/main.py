from pymongo import MongoClient
import json


def cred_db ():
  # MongoDB connection details
  MONGO_URI = "mongodb://admin:password@10.192.36.4:27017/"
  DB_NAME = "Loto"
  COLLECTION_NAME = "cred"

  # Connect to MongoDB
  client = MongoClient(MONGO_URI)
  db = client[DB_NAME]
  collection = db[COLLECTION_NAME]

  # Query a document (modify the filter as needed)
  query_filter = {}  # Fetch all documents, modify as needed (e.g., {"username": "admin"})
  result = collection.find_one(query_filter)
  client.close()
  if result:
    return result
  else:
     return None


result = cred_db()
domain = result["domain"]
jerry = result["jerry"]
donald = result["donald"]
popepy = result["popepy"]
thanos = result["thanos"] 
dc =result["dc"]
ds =result["ds"]
folder_path =result["folder_path"]
folder =result["folder"]
vc_server =result["vc_server"]
username =result["username"]
password =result["password"]
server_list =result["server_list"]