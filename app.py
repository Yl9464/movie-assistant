import logging
import streamlit as st
from streamlit_chatbox import ChatBox
from functions import generate_rag_answer
import streamlit as st
from ollama import ResponseError, chat

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Movie Recommendation Assistant",
    page_icon="🎬",
    layout="centered",
)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

OLLAMA_MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """
You are a helpful movie recommnedation Movie Recommendation Assistant.

Your role is to recommend movies to the user, return the titles and assoicated 
data in response to the inquiry. 


Be clear, concise, and supportive.

Do not invent movies or make alter movie information.

If a question requires information that has not been provided,
say that you do not have enough verified information.
"""


# ---------------------------------------------------------
# Ollama function
# ---------------------------------------------------------

def generate_response(
    messages: list[dict[str, str]]
) -> str:
    """
    Send the conversation to Ollama
    and return the assistant response.
    """

    try:
        response = chat(
            model=OLLAMA_MODEL,
            messages=messages,
            options={
                "temperature": 0.3,
                "top_p": 0.9,
            },
        )

        return response["message"]["content"]

    except ResponseError as error:
        if error.status_code == 404:
            return (
                f"The model '{OLLAMA_MODEL}' is not installed. "
                f"Run this command in Terminal:\n\n"
                f"`ollama pull {OLLAMA_MODEL}`"
            )

        return f"Ollama error: {error.error}"

    except Exception:
        return (
            "I could not connect to Ollama. "
            "Make sure Ollama is installed and running."
        )


# ---------------------------------------------------------
# Initialize conversation history
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am your Movie Recommendation Assistant. "
                "How can I help you today?"
            ),
        }
    ]


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("Movie Recomendation Assistant")

    st.markdown(
        """
Try questions such as:

- Describe a movie to me 
- Provide a list of scary movies.
- What family friendly movies would you reccomend?
- What movie should I choose for a Halloween party?
- Show me movies from 2020 staring Ellen Page
"""
    )

    st.divider()

    if st.button("Clear conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your Movie Recomendation Assistant. "
                    "How can I help you today?"
                ),
            }
        ]

        st.rerun()


# ---------------------------------------------------------
# Main interface
# ---------------------------------------------------------

st.title("🎓 Movie Recommendation Assistant")

st.caption(
    "A simple local AI assistant powered by Ollama."
)


# ---------------------------------------------------------
# Display conversation history
# ---------------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# Accept user input
# ---------------------------------------------------------

question = st.chat_input(
    "Ask the Movie Recommendation Assistant a question"
)


# ---------------------------------------------------------
# Process the question
# ---------------------------------------------------------

if question:
    cleaned_question = question.strip()

    if not cleaned_question:
        st.warning("Please enter a question.")

    elif len(cleaned_question) > 500:
        st.warning(
            "Please keep your question under 500 characters."
        )

    else:
        user_message = {
            "role": "user",
            "content": cleaned_question,
        }

        st.session_state.messages.append(
            user_message
        )

        with st.chat_message("user"):
            st.markdown(cleaned_question)

        model_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        # Limit the amount of history sent to Ollama.
        model_messages.extend(
            st.session_state.messages[-10:]
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = generate_response(
                    model_messages
                )

            st.markdown(answer)

        assistant_message = {
            "role": "assistant",
            "content": answer,
        }

        st.session_state.messages.append(
            assistant_message
        )
# st.set_page_config(
#     page_title="Movie Recommendation Assistant",
# )

# st.title("🎬 Movie Recommendation Assistant")

# chat_box = ChatBox()
# chat_box.init_session()

# # Display previous messages
# chat_box.output_messages()

# # User input
# question = st.chat_input("Ask me about movies...")

# if question:
#     # Display user message
#     chat_box.user_say(question)

#     # Generate RAG response
#     answer = generate_rag_answer(question)

#     # Extract answer
#     response = answer["answer"]

#     # Display assistant response
#     chat_box.ai_say(response)

#     # Refresh UI
#     st.rerun()
    
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
    
