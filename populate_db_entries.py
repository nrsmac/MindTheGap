from faker import Faker
import os
from db import db
db = db()

fake = Faker(locale='en_US')
Faker.seed(0)


with open('./prompt.txt', 'r') as f:
    prompt = f.read()

# Create a generator of all files in entries directory 
# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
entry_files = (entry for entry in os.scandir('./entries') if entry.is_file())

#TODO insert tags
posts_id = []
for file in entry_files:
    with open(file, 'r') as f:
        entry = f.read() 
        document = {
            'creationDate':fake.date_time_between(start_date='-1y', end_date='now'),
            'content':entry.replace(prompt+'\n',""),
            'source':'gpt-j-6b',
            'prompt':'''Write a journal entry of at least 200 words\n\nAnswer:''',
            'kind':'journal'
            } 
        post_id = db.insert_one(document)
        posts_id.append(post_id)

print(f"Added {len(posts_id)} fake entries")