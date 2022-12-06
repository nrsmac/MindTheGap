from faker import Faker
import csv
from tqdm import tqdm
from MTGDatabase import MTGDatabase
MTGDatabase = MTGDatabase()

fake = Faker(locale='en_US')
Faker.seed(0)

with open('./medium_articles.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip header

    documents = []
    for row in tqdm(reader):
        entry = row[0] 
        title,text,url,authors,timestamp,tags = row
        document = {
            'creationDate':timestamp,
            'content':f"{title}\n{text}",
            'kind':'medium article',
            'source':url,
            'tags':tags.split(',')
        }
        documents.append(document)
    MTGDatabase.insert_many(documents)

print(f"Added {len(documents)} fake entries")