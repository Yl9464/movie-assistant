#StreamLit
import streamlit as st
from functions import *

st.title("Movie Recommnedation Assistant")
if st.button("Reload App"):
    st.rerun()
    
question = st.text_input("Ask about movies")

if st.button("Search"):
    result = generate_rag_answer(question, 3)
    st.write(result) #Display LLM resposne
    
    
#     # interactive assistance
# while True:
#     question = input(
#         "\nAsk a campus question or type exit: "
#     )

#     if question.lower().strip() in {
#         "exit",
#         "quit"
#     }:
#         print("Campus Assistant closed.")
#         break

#     result = generate_rag_answer(
#         question,
#         number_of_results=3
#     )

#     print("\nAssistant:")
#     print(result["answer"])

#     print("\nRetrieved Sources:")

#     for index, document in enumerate(
#         result["documents"]
#     ):
#         print(
#             f"{index + 1}. {document}"
#         )