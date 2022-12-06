import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec
#https://medium.com/red-buffer/doc2vec-computing-similarity-between-the-documents-47daf6c828cd

def train(data):
    # Tagging each document 
    print("training")
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

    model = gensim.models.doc2vec.Doc2Vec(vector_size=30, min_count=2, epochs=80)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.save("./doc2vec/doc2vec_tutorial.model")


def load_model(model_name):
    model = Doc2Vec.load(model_name)
    return model

data = ["The process of searching for a job can be very stressful, but it doesn’t have to be. Start with a\
        well-written resume that has appropriate keywords for your occupation. Next, conduct a targeted job search\
        for positions that meet your needs.",
        "Gardening in mixed beds is a great way to get the most productivity from a small space. Some investment\
        is required, to purchase materials for the beds themselves, as well as soil and compost. The\
        investment will likely pay-off in terms of increased productivity.",
        "Looking for a job can be very stressful, but it doesn’t have to be. Begin by writing a good resume with\
        appropriate keywords for your occupation. Second, target your job search for positions that match your\
        needs."]

train(data)
model = load_model("doc2vec/doc2vec_tutorial.model")

similar_doc = model.docvecs.most_similar('0')
print(similar_doc[0])

test_data = word_tokenize("When your focus is to improve employee performance, it’s essential to encourage ongoing\
                        dialogue between managers and their direct reports. Some companies encourage supervisors\
                        to hold one-on-one meetings with employees as a way to facilitate\
                        two-way communication.".lower())

inferred_vector = model.infer_vector(test_data)
# Get most similar document given the inferred vector
sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
print(sims)
