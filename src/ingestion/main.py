import os
from concurrent.futures import ProcessPoolExecutor
from src.ingestion.chunking import sentence_aware_chunker
from src.ingestion.ingestion import ingest_chunks_to_chromadb

import nltk
nltk.download('punkt_tab')

def process_single_file(filename, directory):
    print(f"Processing: {filename}")

    path = os.path.join(directory, filename)
    with open(path, 'r') as file:
        content = file.read()
        
    # Heavy lifting happens here in a separate process
    print(f"Obtaining Document Chunks for {filename}")
    document_chunks = sentence_aware_chunker(content, max_chunk_size=500, overlap_sentences=1)
    print(f"Document Chunks Obtained for {filename}")
    
    # Ingest to ChromaDB
    ingest_chunks_to_chromadb(document_chunks, filename)

    print(f"Finished Processing: {filename}")

    return f"Finished {filename}"

def parallel_chunking_and_ingestion():
    print("#" * 100)
    print("Started Parallel Chunking and Ingestion")

    directory = 'src/ingestion/dataset'
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    print("Obtained all files for chunking")
    print(f"Number of files: {len(files)}")
    print()

    print("Starting processing all files")

    for i, file in enumerate(files):
        results = process_single_file(file, directory)
        print(results)
        print(f"{i + 1} out of {len(files)} processed.")
        print()
    
    print("Ended Parallel Chunking and Ingestion")
    print("#" * 100)

parallel_chunking_and_ingestion()