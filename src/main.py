from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from rag_utils import ingest_document, query_vector_db
from gemini_utils import generate_questions
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/generate-questions/")
async def generate_questions_endpoint(file: UploadFile = File(...), topic: str = Form(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 1: Ingest lecture slides
    ingest_document(file_path)

    # Step 2: Retrieve relevant chunks using topic
    relevant_chunks = query_vector_db(topic)

    # Step 3: Generate questions using Gemini API
    questions = generate_questions(relevant_chunks, topic)

    os.remove(file_path)
    return JSONResponse(content={"questions": questions})
