SYSTEM_PROMPT = """
You are a Movie Recommendation assistant.
"""

def create_grounded_prompt(
    question,
    context
):
    return f"""
Context:

{context}

Question:

{question}

Answer only from the context.
"""