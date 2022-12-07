import streamlit as st
from similarity_tfidf import TFIDFSimilarity
from MTGDatabase import MTGDatabase

def display_document(document):
    title, content = document['content'].split('\n', 1) 
    st.write(f'##### {title}')
    st.write(content[:500]+"...")
    # st.write(document['source'])
    st.write('---')

def get_similar_articles(new_document):
    s = st.write('### Similar Documents')
    with st.spinner(text='Initializing similarity model...'):
        T = TFIDFSimilarity(db)
    with st.spinner(text='Finding similar document ids with tf-idf...'):
        similar_document_ids = T.get_similar_document_ids(new_document)
    with st.spinner(text='Finding similar documents from database...'):
        similar_documents = [T.db.find_by_id(id) for id in similar_document_ids] 
        for document in similar_documents:
            display_document(document) 

def update_db_collection():
    global db
    db = MTGDatabase(collection_selection)

db = MTGDatabase('medium')

'# Similarity'
'Write a new note to compare with your notes'

collection_selection = st.selectbox(
    'Select Corpus:',
    ('None', 'notes','medium'),on_change=update_db_collection)

new_article = st.text_area('New Article', placeholder='Write your article here', height=200)

# Display a button only if the text area is not empty.
if new_article:
    if st.button('Get similar documents'):
        get_similar_articles(new_article) 

