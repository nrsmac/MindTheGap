from faker import Faker
import csv
from MTGDatabase import MTGDatabase
MTGDatabase = MTGDatabase()

fake = Faker(locale='en_US')
Faker.seed(0)

with open('./journal_entries.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip header
    documents = []
    for row in reader:
        entry = row[0] 
        document = {
            'creationDate':fake.date_time_between(start_date='-1y', end_date='now'),
            'content':entry,
            'kind':'journal entry',
            'source':'kaggle journals'
        }
        documents.append(document)
    MTGDatabase.insert_many(documents)

print(f"Added {len(documents)} fake entries")