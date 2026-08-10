import streamlit as st
from streamlit_chatbox import ChatBox
from functions import generate_rag_answer

st.set_page_config(
    page_title="Movie Recommendation Assistant",
)

st.title("🎬 Movie Recommendation Assistant")

chat_box = ChatBox()
chat_box.init_session()

# Display previous messages
chat_box.output_messages()

# User input
question = st.chat_input("Ask me about movies...")

if question:
    # Display user message
    chat_box.user_say(question)

    # Generate RAG response
    answer = generate_rag_answer(question)

    # Extract answer
    response = answer["answer"]

    # Display assistant response
    chat_box.ai_say(response)

    # Refresh UI
    st.rerun()
    
# #StreamLit
# import streamlit as st
# from functions import *

# # for numbers, st.dataframe with Pandas 
# # styling for tables, or st.json for dictionaries.
# # Always map raw data types directly to their 
# # matching UI elements before rendering.

# st.title("Movie Recommnedation Assistant")
# if st.button("Reload App"):
#     st.rerun()
    
# question = st.text_input("Ask about movies")

# if st.button("Search"):
#     result = generate_rag_answer(question, 3)
#     st.write("Summary: ", result["answer"]) #Display LLM resposne
#     st.write("Metadata: ", result["metadata"])
    
