import streamlit as st
from datetime import datetime
from time import sleep
from MTGDatabase import MTGDatabase
from similarity_tfidf import TFIDFSimilarity

db = MTGDatabase('notes')

def get_recent_notes(n=20):
    return db.find_many(n=n).sort('creationDate', -1)

def init_sidebar():
    with st.sidebar:
        '# MindTheGap'
        '### Hi, Noah'
        f'{datetime.now().strftime("%A, %B %d, %Y")}'
        recent_notes_expander = st.checkbox('Recent Notes', value=True) 
    return recent_notes_expander

def update_recent_notes(recent_notes_expander):
    with st.sidebar:
        # x = st.write('...')
        recent_notes_expander = st.empty()
        sleep(1)
        # x = st.empty()
        recent_notes = get_recent_notes()
        # set checkbox to be automatically enabled
        if recent_notes_expander:
            for note in recent_notes:
                # place into a box
                max_title_display_length = 40
                title = note["title"] if len(note["title"]) < max_title_display_length else note["title"][:max_title_display_length]+"..."
                date = note["creationDate"].strftime("%a %m/%d")

                with st.expander(f'{title} - {date}'):
                    st.markdown(note['content'][:200]+"...")
    

def get_similar_articles(new_document):
    with st.spinner(text='Initializing similarity model...'):
        T = TFIDFSimilarity(db)
    with st.spinner(text='Finding similar document ids with tf-idf...'):
        similar_document_ids = T.get_similar_document_ids(new_document)
    with st.spinner(text='Finding similar documents from database...'):
        similar_documents = [T.db.find_by_id(id) for id in similar_document_ids] 
        for document in similar_documents:
            display_document(document) 


def submit_note(title, entry):
    db.insert_one({
        'title': title, 
        'content': entry, 
        'creationDate': datetime.now()})

recent_notes_expander = init_sidebar() 
update_recent_notes(recent_notes_expander)
new_title = st.text_input('Title', placeholder='Title', value='Untitled', max_chars=100)
new_entry = st.text_area('New Note', placeholder='Write your note here', height=200)

# Display a button only if the text area is not empty.
if st.button('Save Note') and new_entry and new_title:
    recent_notes_expander = st.empty()
    update_recent_notes(recent_notes_expander)
    submit_note(new_title, new_entry)
    # Empty the text areas
    new_title = st.empty()
    new_entry = st.empty()