import chromadb

def retrieve_documnents(queries, n_results=3):
    # Initialise local persistent client. my_local_rag_db folder created.
    client = chromadb.PersistentClient(path="src/my_local_rag_db")

    collection = client.get_collection(name="document_collection")
    
    results = collection.query(
        query_texts=queries,
        n_results=n_results,
        include=["documents", "metadatas", "distances", "embeddings"]
    )

    # Sanity check
    space = collection.metadata.get("hnsw:space", "l2")  # default is l2
    print(f"Collection Space Used: {space}")
    if space != "cosine":
        raise ValueError(f"Collection uses '{space}' distance, not cosine.")

    # Consolidating retrieved documents and their similarity score
    retrieved_content = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        similarity = 1 - dist
        print(f"[Score: {similarity:.2f}] Found in: {meta['source']}")
        retrieved_content.append(str({'source': meta['source'], 'document': doc}))
    
    return retrieved_content
