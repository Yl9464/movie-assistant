import logging
from sentence_transformers import SentenceTransformer
from database import collection
from ollama import chat
from time import perf_counter
from config import *
from database import *
#Temp
TEMPERATURE = 0.2

EVALUATION_SCALE_MIN = 1
EVALUATION_SCALE_MAX = 5

#word based chunking
def split_text_into_chunks(
    text,
    chunk_size=30,
    overlap=5
):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

# retrieval function
def retrieve_context(
    question,
    number_of_results=3
):
    logging.info("Entered retrieve_context()")
    
    question_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(query_embeddings=[question_embedding], n_results =number_of_results)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return documents, metadatas, distances

def generate_rag_answer(question, number_of_results=3):
    logging.info("Entered generate_rag_answer()")    
    documents, metadatas, distances = retrieve_context(
        question,
        number_of_results
    )
    context = "\n\n".join(documents)
    
    #Build Prompt
    prompt = f"""
    You are a movie recommendation assistant.

    Answer the question using only the context below.

    If the answer is not available in the context, say:
    "I do not have enough verified information to answer
    that question."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    #send promt ot LLM
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.2
        }
    )

    answer = response["message"]["content"]

    return {
        "question": question,
        "answer": answer,
        "documents": documents,
        "metadata": metadatas,
        "distances": distances
    }
def generate_response( prompt,temperature=TEMPERATURE):
    start_time = perf_counter()

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": temperature
        }
    )

    elapsed_time = perf_counter() - start_time

    return {
        "text": response["message"]["content"],
        "response_time": elapsed_time
    }