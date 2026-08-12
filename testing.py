from functions import *

#RAG Testing
questions = [
    "Recommend some good movies" #weak prompt
    "When was the film Avatar: The Blue People With Tails released" #hallucination
    "Give a list of movies released in 2030" #hallucination
    "Recommend 3 mind-bending sci-fi movies released after 2010 that feature plot twists." #zero shot
    "Recommend a movie for a cozy rainy day", #First-Shot
    "Summarize Toy Story's plot in exactly six words", ##First-Shot
    "Brainstorm a movie about a talking dog who can time travel using a magic bone. Describe its opening scene." #Top-P
]

for q in questions:
    test_case =generate_rag_answer(q, 3)
   
    print(test_case)
    print("-" * 60)
    
# for document, metadata, distance in zip(
#     documents,
#     metadatas,
#     distances
# ):
    # print(document)
    # print(metadata)
    # print(distance)
    # print("-" * 60)