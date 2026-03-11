import chromadb
from sentence_transformers import SentenceTransformer

# Initialise local persistent client. my_local_rag_db folder created.
client = chromadb.PersistentClient(path="src/my_local_rag_db")

# SentenceTransformers embedding function
model = SentenceTransformer('all-MiniLM-L6-v2')

collection = client.get_or_create_collection(
    name="document_collection", 
    # Cosine Similarity Search
    metadata={"hnsw:space": "cosine"}
)

def ingest_chunks_to_chromadb(chunks, doc_name):
    # Chunked documents generated from chunking.py ingested to chromadb with vector embeddings of documents.
    ids = [f"{doc_name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": doc_name} for _ in range(len(chunks))]
    embeddings = model.encode(chunks).tolist()
    
    collection.add(
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully ingested {len(chunks)} chunks.")
