import os
from huggingface_hub import InferenceClient
from src.retrieval import retrieve_documnents


def llm_api(query):
    client = InferenceClient()
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
    )

    return completion.choices[0].message

def llm_rag_generation_documents(user_query):
    # Step 1: Retrieve Documents from ChromaDB via Cosine Similarity
    documents = retrieve_documnents(user_query)
    # New Line Spacing For each Document/Chunk
    context_text = "\n---\n".join(documents)
    print(context_text)
    
    #Step 2: Setup RAG Prompt for LLM API
    rag_prompt = f"""
    You are a helpful assistant. Answer the question using ONLY the provided context below.
    If the answer is not in the context, say that you don't know. Additionally, you also NEED
    to include the source of the document, as a way to cite where the information from the context
    is coming from. So again, if there is no 'source' associated with the documents, say you don't 
    know the answer.

    Context:
    {context_text}

    Question: 
    {user_query}

    Answer:
    """
    
    response = llm_api(rag_prompt)
    return response
    # return "dummy"
