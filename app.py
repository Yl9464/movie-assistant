#StreamLit
import streamlit as st
from functions import *

# for numbers, st.dataframe with Pandas 
# styling for tables, or st.json for dictionaries.
# Always map raw data types directly to their 
# matching UI elements before rendering.

st.title("Movie Recommnedation Assistant")
if st.button("Reload App"):
    st.rerun()
    
question = st.text_input("Ask about movies")

if st.button("Search"):
    result = generate_rag_answer(question, 3)
    st.write("Summary: ", result["answer"]) #Display LLM resposne
    st.write("Metadata: ", result["metadata"])
    
