import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec
from MTGDatabase import MTGDatabase

MTGDatabase = MTGDatabase()

def train(data):
    # Tagging each document 
    print("training")
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

    model = gensim.models.doc2vec.Doc2Vec(vector_size=100, window=10, min_count=1, workers=8, alpha=0.025, min_alpha=0.015, epochs=80)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    path = "doc2vec.model" 
    print(f"Saving to {path}")
    model.save(path)
    # Return indexes of all documents corresponding with their mongodb object id
    return [doc.tags[0] for doc in tagged_data]

# Get all documents from db
cursor = MTGDatabase.get_all_documents()
# unpack cursor
documents = [doc for doc in cursor]
ids, contents = [doc['_id'] for doc in documents], [doc['content'] for doc in documents] 

indexes = train(contents)
print(list(zip(ids, indexes)))