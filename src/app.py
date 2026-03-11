from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.generation import llm_rag_generation_documents

app = FastAPI()

# Only User Query Allowed
class QueryRequest(BaseModel):
    query: str

# Post Request starting the whole RAG processes, returning the response from the LLM
@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        response = llm_rag_generation_documents(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000)