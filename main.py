from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from rag_system import load_and_split_documents, create_vector_store, setup_rag_chain

#Initialize the API
app = FastAPI()

class Query(BaseModel):
    question: str

try:
    FILE_PATH = "knowladge.txt"
    if not os.path.esists(FILE_PATH):
        with open(FILE_PATH, "W") as f:
            f.write("FastAPI")
    chunks = load_and_split_documents(FILE_PATH)
    vector_store = create_vector_store(vector_store)
except Exception as e:
    raise RuntimeError(f"Failed to initialize RAG : {e}")  

@app.post("/ask")
async def ask_question(query: Query):
    try:
        result = qa_chain.invoke({"query": query.question})
        return {"response": result["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     


# run the app with: uvicorn main:app --reload                         


