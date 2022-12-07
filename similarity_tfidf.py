from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from MTGDatabase import MTGDatabase

class TFIDFSimilarity:
    def __init__(self, db, n=4000, documents=None):
        self.db = db 
        self.vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        if not documents:
            self.documents = self._get_documents_from_db(n)
        else:
            self.documents = documents

    def _get_documents_from_db(self, n):
        # Populate the database with n documents from database 
        # TODO do this in a background thread
        return [doc for doc in self.db.find_many(n=n)]

    def add_document_to_similarity_matrix(self, document):
        '''Doesn't add document to server, just to the similarity matrix'''
        self.vectorizer = TfidfVectorizer()
        contents = [doc['content'] for doc in self.documents]
        contents.append(document)
        self.tfidf_matrix = self.vectorizer.fit_transform(contents)
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def get_similar_document_ids(self, new_document, n=5):
        self.add_document_to_similarity_matrix(new_document)
        idx = -1 # last document we appended
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1] # remove the first one, which is the document itself
        document_indices = [i[0] for i in sim_scores]
        return [self.documents[i]['_id'] for i in document_indices]
    
    def get_similar_document_contents(self, new_document, n=5):
        similar_document_ids = self.get_similar_document_ids(new_document, n)
        similar_documents = [self.db.find_by_id(id) for id in similar_document_ids] 
        return [s['content'] for s in similar_documents]

def main():
    T = TFIDFSimilarity()
    new_document = input("New document: ")
    similar_document_ids = T.get_similar_document_ids(new_document)
    similar_documents = [T.db.find_by_id(id) for id in similar_document_ids] 
    print("Similar documents:")
    [print(s['content'].partition('\n')[0]) for s in similar_documents]

if __name__ == "__main__":
    main()