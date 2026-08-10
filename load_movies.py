import logging
import os
import pandas as pd
import kagglehub
from functions import *
from database import *
from config import *
# Download and load dataset
# -----------------------------
print("Downloading dataset...")

path = kagglehub.dataset_download(
    "sharmaabhi04/100k-movies-dataset"
)

file_path = os.path.join(
    path,
    "100k_Movies_dataset.csv"
)

movies_df = pd.read_csv(file_path)
print(f"Loaded {len(movies_df)} movies.")

# -----------------------------
# Build chunks
# -----------------------------
all_chunks = []
all_metadata = []


chunk_id = 0  # Global chunk counter

for index in movies_df.itertuples(index=True):

    chunks = split_text_into_chunks(
        index.title,
        chunk_size=100,
        overlap=20
    )

    for chunk in chunks:
        all_chunks.append(chunk)
        all_metadata.append({
            "runtime": index.runtime,
            "genre": index.genre,
            "ratings": index.ratings,
            "director": index.director,
            "cast": index.cast,
            "Description": index.Description,
            "released_year": index.released_year,
            "chunk_id": chunk_id
        })
        chunk_id += 1  # Increment after each chunk
        
print("Total CSV chunks:", len(all_chunks))

# IDs and metadata creation
chunk_ids = [
    f"chunk_{index}"
    for index in range(len(all_chunks))
]

metadata = [
    {
        "source": "movie_dataset",
        "chunk_number": index
    }
    for index in range(len(all_chunks))
]


print("\nChunks created with lengths:") 
print("Ids =", len(chunk_ids), " || metadata: ", len(metadata))


# -----------------------------
# Store in ChromaDB
# -----------------------------

from time import perf_counter

batch_size = 5000
total_documents = len(all_chunks)

start_time = perf_counter()

for start in range(0, total_documents, batch_size):
  
    batch_start_time = perf_counter()
    end = min(start + batch_size, total_documents)

    collection.add(
        ids=chunk_ids[start:end],
        documents=all_chunks[start:end],
        metadatas=all_metadata[start:end]
    )

    batch_time = perf_counter() - batch_start_time
    progress = (end / total_documents) * 100

    print(
        f"Batch {start//batch_size + 1}: "
        f"{start:,}-{end:,} "
        f"| {progress:.2f}% "
        f"| Time: {batch_time:.2f}s"
    )

total_time = perf_counter() - start_time

print(f"\nCompleted in {total_time:.2f} seconds")
print("Documents stored in ChromaDB.")
print("Collection size:", collection.count())
