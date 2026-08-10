# 🎬 Movie Recommendation Assistant

A local, privacy-friendly movie recommendation chatbot built with **Retrieval-Augmented Generation (RAG)**. It answers questions using a 100k-movie dataset, retrieves relevant context with **ChromaDB** vector search, and generates grounded answers using a local **Ollama** LLM — all through a **Streamlit** chat interface.

No data leaves your machine: the LLM, embeddings, and vector store all run locally.

---

## How it works

1. **Dataset** — a 100k-movie CSV (title, genre, rating, director, cast, description, etc.) is downloaded via `kagglehub`.
2. **Chunking** — movie titles are split into overlapping word chunks and paired with their metadata.
3. **Embedding** — each chunk is embedded with the `all-MiniLM-L6-v2` sentence-transformer model.
4. **Vector store** — embeddings are stored in a local, persistent **ChromaDB** collection.
5. **Retrieval** — when you ask a question, it's embedded and matched against the collection to pull the most relevant chunks.
6. **Generation** — the retrieved context is inserted into a grounded prompt and sent to a local **Ollama** model (`llama3.2:3b` by default), which is instructed to answer only from that context.

---

## Requirements

- **Python** 3.10–3.11 (recommended)
- **Ollama** installed and running locally — [ollama.com](https://ollama.com)
- ~4 GB free disk space for the dataset, embedding model, and vector index
- A Kaggle account is **not** required for the dataset download (handled by `kagglehub`), but you'll need internet access the first time you run the app

---

## Installation

### 1. Clone or download the project files

Make sure you have these two files together in a project folder:

```
movie-assistant/
├── streamlit_app.py
└── requirements.txt
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
pip install kaggle sentence-transformers chromadb

```

### 4. Install and start Ollama

Download Ollama for your OS from [ollama.com/download](https://ollama.com/download), then pull the model used by the app:

```bash
ollama pull llama3.2:3b
```

Ollama runs as a background service after installation. Verify it's running:

```bash
curl http://localhost:11434
```

You should get a response (not a connection error). On some systems you may need to start it manually:

```bash
ollama serve
```

### 5. Run the app

From the project folder:

```bash
streamlit run streamlit_app.py
```

Streamlit will open the app in your browser at `http://localhost:8501`.

---

## First run notes

- The **first launch** will take a few minutes: it downloads the dataset, loads the embedding model, and builds the ChromaDB vector index for all movie chunks.
- This index is cached (`st.cache_resource`) for the life of the Streamlit process, and also persisted to disk in a local `./chroma_db` folder — subsequent app restarts still re-embed in-process but reuse the same on-disk Chroma path.
- If you change the dataset or chunking logic, delete the `./chroma_db` folder before restarting so the index rebuilds from scratch.

---

## Using the app

- Type a question or preference in the chat box, e.g.:
  - *"Recommend 5 sci-fi movies similar to Interstellar"*
  - *"I want a family-friendly comedy, avoid R-rated movies"*
  - *"What should I watch if I only have 90 minutes?"*
- Expand **"Sources used"** under any answer to see which movie chunks were retrieved and how relevant they were (distance score — lower is more similar).
- Use the **sidebar** to:
  - Confirm Ollama is running
  - Adjust the response **temperature** (higher = more creative/less deterministic)
  - Adjust how many chunks are **retrieved** per question
  - View the system prompt
  - Clear the conversation

---

## Configuration

You can adjust these constants near the top of `streamlit_app.py`:

| Setting | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `llama3.2:3b` | Any model you've pulled with `ollama pull` |
| `TEMPERATURE_DEFAULT` | `0.2` | Default generation temperature |
| `CHUNK_SIZE` | `100` | Words per chunk |
| `CHUNK_OVERLAP` | `20` | Word overlap between chunks |
| `N_RESULTS_DEFAULT` | `3` | Chunks retrieved per query |

To use a different Ollama model, pull it first (e.g. `ollama pull llama3.1:8b`) and update `OLLAMA_MODEL`.

---

## Troubleshooting

**"Ollama is NOT running" in the sidebar**
Ollama isn't reachable at `http://localhost:11434`. Start the Ollama app or run `ollama serve`, then reload the page.

**App hangs or is very slow on first run**
This is expected — it's downloading the dataset and embedding ~100k movie titles. Subsequent interactions within the same session are fast since the index is cached.

**`kagglehub` download fails**
Check your internet connection. Some networks block Kaggle's CDN; try a different network or VPN if the download consistently times out.

**Answers say "I do not have enough verified information..."**
This means the retrieved context didn't contain a relevant answer — try rephrasing, or increase the "Chunks to retrieve" setting in the sidebar.

**Out-of-memory or very slow embedding step**
Embedding the full dataset uses your CPU (or GPU, if `sentence-transformers` detects one). On low-memory machines, consider reducing the dataset size or using a smaller embedding model.

**Stale results after editing the code**
Streamlit caches `@st.cache_resource` functions. Click **"Clear cache"** from Streamlit's menu (top-right ⋮) or restart the app after changing dataset/chunking/embedding logic.

---

## Project structure

```
movie-assistant/
├── streamlit_app.py     # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md              # This file
└── chroma_db/             # Auto-created local vector store (persisted)
```

---

## Notes on the original notebook

This app is adapted from `MovieAssistant.ipynb`, which developed the RAG pipeline interactively and included exploratory testing cells (prompt-style comparisons, hallucination checks, few-shot examples). Those experiments aren't part of the app — the app keeps the core grounded retrieval-and-generation logic (`retrieve_context` + `generate_rag_answer`) and wraps it in an interactive chat UI.
