import chromadb
from config import *

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    COLLECTION_NAME
)