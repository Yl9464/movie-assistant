## Zero-Shot Prompting (Lensi)
Implemented and tested 5 zero-shot prompts for the movie assistant, covering common user requests without providing example responses:
- Recommend a movie for a rainy day
- What's a good movie to watch with my parents?
- Suggest a movie similar to Inception
- Give me a movie recommendation for someone who likes slow-burn dramas
- What should I watch if I only have 90 minutes free?

Each prompt was run against the Llama 3.2 (3B) model via Ollama and evaluated for accuracy and relevance. Most prompts returned strong, on-topic recommendations with real movie titles; the "90 minutes" prompt revealed a limitation where the model interpreted runtime constraints loosely, suggesting short-form content instead of full movies.

## Streamlit User Interface (Lensi)
Built a Streamlit-based chat interface (`app.py`) for the Movie Recommendation Assistant, including:
- Multi-turn conversation support using `st.session_state`
- Real-time chat display with `st.chat_message`
- Integration with the Ollama-hosted Llama 3.2 model
- Deployed locally via Colab and exposed through a public tunnel (localtunnel) for testing

The interface successfully handles user input, maintains conversation history, and returns accurate movie recommendations.
