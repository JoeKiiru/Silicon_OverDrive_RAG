import chromadb
from chromadb.utils import embedding_functions

# Initialise local persistent client. my_local_rag_db folder created.
client = chromadb.PersistentClient(path="src/my_local_rag_db")

# SentenceTransformers embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="document_collection", 
    embedding_function=default_ef,
    metadata={"hnsw:space": "cosine"}
)

results = collection.query(
    query_texts=["Who is Trevor?"],
    n_results=2
)

for doc in results['documents'][0]:
    print(f"Retrieved Context: {doc}")
