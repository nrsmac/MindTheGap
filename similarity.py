import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from MTGDatabase import MTGDatabase

class Similarity():
    def __init__(self):
        self.db = MTGDatabase()
        self.documents = [doc for doc in self.db.get_all_documents()]
        self.ids = [doc['_id'] for doc in self.documents]

        self.model = Doc2Vec.load("doc2vec.model") 
        # TODO fix, not robust at all
        self.tag_to_id = {tag: id for tag, id in zip(range(len(self.ids)), self.ids)}

    def get_similar_documents(self, text, n=5):
        inferred_vector = self.model.infer_vector(text)
        sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))[:n]
        similar_ids = [self.tag_to_id[int(s[0])] for s in sims]
        print(similar_ids)
        similar_docs = [self.db.find_by_id(id) for id in similar_ids] 
        return similar_docs

if __name__ == "__main__":
    s = Similarity()
    # text = input("Enter text to find similar documents:")
    text = "The world is growing ever larger. " 
    similarities = s.get_similar_documents([text])
    for i, similarity in enumerate(similarities):
        print(f"--{i}--\n{similarity['content']}")
    
