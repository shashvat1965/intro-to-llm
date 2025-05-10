import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBuFDI0ClvxUEnRPaHkljJh4r_vvY7dbI0")

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_questions(chunks, topic):
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful educational assistant. Based on the following reference material, generate 5 exam-level questions on the topic "{topic}". The questions should be concise and test understanding.

Reference Material:
{context}

Questions:
"""
    response = model.generate_content(prompt)
    print(response.text.strip().split("\n"))
    return response.text.strip().split("\n")
