from pymongo import MongoClient
from datetime import datetime
from MTGDatabase import MTGDatabase

# Connect to the database
db = MTGDatabase()

now = datetime.now()
print(f'{now.ctime()}')
note = input("Enter note content:")

db.insert_one(
    {
        'creationDate':now,
        'content':note   
    }
)