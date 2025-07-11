# db_operations.py

from pymongo import MongoClient
from datetime import datetime
import os
import json

def connect_to_mongo(uri="mongodb://localhost:27017/", db_name="tictavarium", collection_name="sheets"):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]

def insert_documents(json_data, collection, source_pdf):
    # Kaynak adını ve timestamp'i her belgeye ekle
    timestamp = datetime.utcnow()
    for doc in json_data:
        doc["source_pdf"] = source_pdf
        doc["created_at"] = timestamp

    # Önceki verileri sil (aynı kaynaktan gelenler)
    collection.delete_many({"source_pdf": source_pdf})

    # Yeni verileri ekle
    if isinstance(json_data, list):
        collection.insert_many(json_data)
    else:
        collection.insert_one(json_data)

    return len(json_data)

def load_json_file(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def cleanup_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"{path} dosyası silindi.")
    except Exception as e:
        print("Dosya silme hatası:", e)
