from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import answer
from app.ingest import collection

app = FastAPI()

class Question(BaseModel):
    text: str

@app.post("/ask")
async def ask_question(question: Question):
    if not question.text.strip():
        return {"error": "Question is empty."}
    try:
        text, chunks, usage = answer(question.text)
        return {
            "answer": text,
            "sources": chunks,
            "usage": usage
        }
    except Exception as e:
        return {"error": str(e)}

    return {"answer": text, "sources": chunks, "usage": usage}

@app.get("/count")
async def get_count():
    return {"Chunks stored": collection.count()}

