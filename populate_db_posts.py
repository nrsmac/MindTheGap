from pprint import pprint
from faker import Faker
from mdgen import MarkdownPostProvider
from db import db

db = db()
db.drop()

fake = Faker(locale='en_US')
# Change this provider for gpt created posts
fake.add_provider(MarkdownPostProvider)
Faker.seed(0)

fake_notes = [{
    #TODO insert tags
    'creationDate':fake.date_time_between(start_date='-1y', end_date='now'),
    'content':fake.post(size='medium'),
    'source':'mdgen',
    'kind':'post'
    } for x in range(100)]

# pprint(fake_notes)

posts_id = db.insert_many(fake_notes)
print(f"Added {len(posts_id)} fake posts")