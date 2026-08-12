from functions import *
# Questions:
# Zero-Shot Prompts Recommend movies directly without providing any prior examples or demonstrations. 
# Recommend 3 mind-bending sci-fi movies released after 2010 that feature plot twists.
# What are some critically acclaimed heist movies where the main characters try to steal a painting?


#First-Shot PromptsDefinition: A specific subset of few-shot prompting where exactly 
#"Recommend a movie for a cozy rainy day" -> Recommendation: Knives Out (2019) – A cozy, sweater-heavy mystery set in a sprawling autumnal estate.Vibe: "High-adrenaline weekend adrenaline rush" -
#Summarize a film's plot in exactly six words, like the example below:Movie: The Matrix -> Hacker discovers reality is a computer simulation.Movie: Jurassic Park 

#High value Top-P value: Model returns diverse and less predictable response. Useful for movie brainstorming and unconventional recommendations.
#Brainstorm an utterly bizarre, surreal concept for an indie film blending time travel and culinary arts, and describe its opening scene."

#RAG Testing
questions = [
    "When was the film Avatar: The Blue People With Tails released" #hallucination
    "Give a list of movies released in 2030" #hallucination
    "Recommend 3 mind-bending sci-fi movies released after 2010 that feature plot twists." #zero shot
    "Recommend a movie for a cozy rainy day", #First-Shot
    "Summarize Toy Story's plot in exactly six words", ##First-Shot
    "Brainstorm a movie about a talking dog who can time travel using a magic bone.Describe its opening scene." #High value Top-P
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