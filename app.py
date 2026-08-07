#StreamLit

import streamlit as st
from functions import generate_rag_answer

st.title("Movie Recommnedation Assistant")

question = st.text_input(
    "Ask about movies"
)

if st.button("Search"):

    answer = generate_rag_answer(question)

    st.write(answer["answer"])