#RAG Testing
system_prompt = """
You are our AI movie recommendation assistant.
Your job is to recommend movies based on user preferences.
You should:
- Ask questions when the user gives unclear preferences.
- Explain why each recommendation matches the user's interests.
- Never invent movies, actors, ratings, or availability.
- Admit when you do not know something.
"""
print("====SYSTEM PROMPT=====")
print(system_prompt)

print("\n===WEAK PROMPTS===\n")
weak_prompts = [
    "Recommend me some movies.",
    "I need a good movie.",
    "What movie should I watch?",
    "Give me something interesting.",
    "Tell me the best movie."
]
print("1. ", weak_prompts[0])
print("2. ", weak_prompts[1])
print("3. ", weak_prompts[2])
print("4. ", weak_prompts[3])
print("5. ", weak_prompts[4])

print("\n===STRONG PROMPTS===\n")

strong_prompts = [
    "Recommend 5 science fiction movies similar to Interstellar. I like space exploration and emotional stories.",

    "I want a family-friendly comedy movie that teenagers and adults can enjoy. Avoid R-rated movies.",

    "I enjoyed Knight and the Seven Kingdoms. Recommend a series with similar themes and storytelling.",

    "Recommend horror movies that focus on suspense instead of gore.",

    "I only have 90 minutes. Recommend highly-rated movies under that runtime."

]
print("1. ", strong_prompts[0])
print("2. ", strong_prompts[1])
print("3. ", strong_prompts[2])
print("4. ", strong_prompts[3])
print("5. ", strong_prompts[4])

print("\n===HALLUCINATION PROMPTS===\n")
hallucination_prompts = [
    "Tell me about the movie The Last Ocean Planet starring Chris Evans.",

    "Why did Titanic 2: Return of the Ocean win Best Picture?",

    "Recommend movies directed by Christopher Nolan before 1900.",

    "What superhero movies did Emily Watson Jr. star in?",

    "Is Avatar 5 currently available on Netflix?"
]
print("1. ", hallucination_prompts[0])
print("2. ", hallucination_prompts[1])
print("3. ", hallucination_prompts[2])
print("4. ", hallucination_prompts[3])
print("5. ", hallucination_prompts[4])

from ollama import chat

print("\n===ZERO-SHOT PROMPTS===\n")

zero_shot_prompts = [
    "Recommend a movie for a rainy day.",
    "What's a good movie to watch with my parents?",
    "Suggest a movie similar to Inception.",
    "Give me a movie recommendation for someone who likes slow-burn dramas.",
    "What should I watch if I only have 90 minutes free?"
]

print("1. ", zero_shot_prompts[0])
print("2. ", zero_shot_prompts[1])
print("3. ", zero_shot_prompts[2])
print("4. ", zero_shot_prompts[3])
print("5. ", zero_shot_prompts[4])

print("\n===ZERO-SHOT RESPONSES===\n")

for i, prompt in enumerate(zero_shot_prompts, start=1):
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.7
        }
    )
    print(f"{i}. PROMPT: {prompt}")
    print(f"   RESPONSE: {response['message']['content']}")
    print("\n")