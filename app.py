import streamlit as st
from streamlit_chatbox import ChatBox
from functions import *
import streamlit as st
from config import *

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Movie Recommendation Assistant",
    page_icon="🎬",
    layout="centered",
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
                answer = streamlit_response(
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
