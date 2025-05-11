### main.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from utils import extract_text_from_pdf, chunk_text, ingest_document, query_vector_db
from gemini_utils import generate_questions
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/generate-questions/")
async def generate_questions_api(
    file: UploadFile = File(...),
    topic: str = Form(...),
    difficulty: str = Form(...),
    number_of_questions: str = Form(...),
    open_book: str = Form(...),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_document(file_path)
    relevant_chunks = query_vector_db(topic)
    questions = generate_questions(relevant_chunks, topic, difficulty, number_of_questions, open_book)
    return JSONResponse(content={"questions": questions})
