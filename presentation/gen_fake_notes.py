from faker import Faker
import os

fake = Faker(locale='en_US')
# Change this provider for gpt created posts
fake.add_provider(MarkdownPostProvider)
Faker.seed(0)

fake_notes = [{
    #TODO insert tags
    'creationDate':fake.date_time_between(start_date='-1m', end_date='now'),
    'content':fake.post(size='medium'),
    } for x in range(100)]

path = 'presentation/fake_notes'
for note in fake_notes:
    # Write each note to a file in fake_notes
    file_name = f'{note["creationDate"].strftime("%Y-%m-%d-%H-%M-%S")}.md'
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as f:
        f.write(note['content'])
