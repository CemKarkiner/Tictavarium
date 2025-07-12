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
    try:
        timestamp = datetime.utcnow()
        if isinstance(json_data, dict):
            json_data = [json_data]
        for doc in json_data:
            doc["source_pdf"] = source_pdf
            doc["created_at"] = timestamp
        collection.delete_many({"source_pdf": source_pdf})
        collection.insert_many(json_data)
        return len(json_data)
    except Exception as e:
        print("DB insert error:", e)
        return 0

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

def get_all_notes_by_pdf(source_pdf, collection):
    try:
        docs = collection.find({"source_pdf": source_pdf}).sort([
            ("part", 1), ("measure", 1)
        ])
        all_notes = []
        for doc in docs:
            all_notes.extend(doc.get("notes", []))
        return all_notes
    except Exception as e:
        print("DB'den nota çekme hatası:", e)
        return []