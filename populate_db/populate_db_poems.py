from MTGDatabase import MTGDatabase
from faker import Faker

fake = Faker(locale='en_US')
Faker.seed(0)

# read in Poetry Foundation CSV and upload to database
import csv
MTGDatabase = MTGDatabase()
with open('./PoetryFoundationData.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip header
    poems = []
    for row in reader:
        _, title, content, author, tags = row
        poem = {
            'creationDate':fake.date_time_between(start_date='-1y', end_date='now'),
            'content':content,
            'author':author,
            'tags':tags,
            'kind':'poem',
            'source':'poetryfoundation'
        }
        poems.append(poem)
    MTGDatabase.insert_many(poems)
    print(f"Added {len(poems)} poems")

