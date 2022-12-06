from pymongo import MongoClient
from datetime import datetime

# Connect to the database
client = MongoClient("mongodb+srv://nrsmac:Nrsmac12@mindthegap.e68yexb.mongodb.net/?retryWrites=true&w=majority")
db = client
collection = db.mtg.notes

now = datetime.now()
print(f'{now.ctime()}')
note = input("Enter note content:")

collection.insert_one(
    {
        'creationDate':now,
        'content':note   
    }
)