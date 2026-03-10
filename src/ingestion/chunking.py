from nltk.tokenize import sent_tokenize

# Checks if it is available first, otherwise downloads punkt_tab.


def sentence_aware_chunker(text, max_chunk_size=500, overlap_sentences=1):
    # Returns a list of sentances, e.g. ["Sentance 1", "Sentance 2", ...]
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_len = len(sentence)
        
        # Checks to see if adding the following sentance exceeds the max_chunk_size
        if current_length + sentence_len > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            
            # Overlap created to ensure prior sentances and their context can be used in subsequent sentances.
            # Keep the last N sentences for context.
            current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
            current_length = sum(len(s) for s in current_chunk)
            
        current_chunk.append(sentence)
        current_length += sentence_len
        
    # Append the final remaining chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
