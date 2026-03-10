import chromadb
from chromadb.utils import embedding_functions

# Initialise local persistent client. my_local_rag_db folder created.
client = chromadb.PersistentClient(path="src/my_local_rag_db")

# SentenceTransformers embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="document_collection", 
    embedding_function=default_ef
)

def ingest_chunks_to_chromadb(chunks, doc_name):
    # Chunked documents generated from chunking.py ingested to chromadb with vector embeddings of documents.
    ids = [f"{doc_name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": doc_name} for _ in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully ingested {len(chunks)} chunks.")
