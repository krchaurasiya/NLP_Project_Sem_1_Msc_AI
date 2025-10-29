import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["law_translate_db"]
collection = db["documents"]

def save_document_record(record):
    return collection.insert_one(record).inserted_id

def get_document(doc_id):
    return collection.find_one({"_id": ObjectId(doc_id)})
