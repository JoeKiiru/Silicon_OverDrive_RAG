import chromadb
from chromadb.utils import embedding_functions

# Initialise local persistent client. my_local_rag_db folder created.
client = chromadb.PersistentClient(path="src/my_local_rag_db")

# SentenceTransformers embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="document_collection", 
    metadata={"hnsw:space": "cosine"}
)

preview = collection.peek(limit=5)
print(preview)