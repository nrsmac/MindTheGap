from pymongo import MongoClient
from bson.objectid import ObjectId
from tqdm import tqdm

class MTGDatabase:
    def __init__(self):

        with open('.connection_url', 'r') as f:
            connection_url = f.read()

        self.client = MongoClient(connection_url)
        connection_url=None

        self.db = self.client
        self.collection = self.db.mtg.notes

    def insert_one(self, document):
        return self.collection.insert_one(document).inserted_id

    def insert_many(self, documents):
        return self.collection.insert_many(documents).inserted_ids

    def find_one(self, query):
        return self.collection.find_one(query)

    def find_by_id(self, id:int):
        return self.find_one({"_id" : ObjectId(id)})

    def find_many(self, query):
        return self.collection.find(query)

    def drop(self):
        self.collection.drop()

    def get_all_documents(self):
        return self.collection.find()