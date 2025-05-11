import google.generativeai as genai

genai.configure(api_key="AIzaSyBuFDI0ClvxUEnRPaHkljJh4r_vvY7dbI0")

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_questions(chunks, topic, difficulty, number_of_questions, open_book):
    context = "\n\n".join(chunks)
    
    open_book_instruction = (
        "Design the questions to test conceptual understanding, application, or analysis, "
        "rather than memorization, since the exam is open book."
        if open_book
        else "Design the questions to test knowledge, recall, and understanding, assuming no access to the reference material."
    )
    
    prompt = f"""You are a precise and helpful educational assistant. Your task is to generate clear and concise exam questions that accurately assess understanding of the provided reference material. Use only the information within the reference and do not infer or fabricate content. Avoid any markdown, special characters, or numbering in your output.

Instructions:
- Generate exactly {number_of_questions} exam questions.
- Difficulty level: {difficulty}
- Topic: "{topic}"
- Format each question as a standalone sentence or directive.
- Avoid repetition across questions.
- Do NOT add any introductory or closing text. Output ONLY the questions as plain text, without numbering.
- {open_book_instruction}

Here are a few examples for guidance:

---
**Reference Material**: Newton's First Law states that an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.  
**Topic**: Newton's First Law  
**Difficulty**: Easy  
**Generated Questions**:  
What does Newton's First Law state about objects in motion?  
Under what condition will an object at rest begin to move according to Newton's First Law?

---
**Reference Material**: A stack is a linear data structure that follows the LIFO (Last In First Out) principle. It supports operations like push, pop, and peek.  
**Topic**: Stack Data Structure  
**Difficulty**: Medium  
**Generated Questions**:  
What is the principle that a stack follows?  
Which stack operation removes the top element from the stack?

Now, generate {number_of_questions} {difficulty}-level questions on the topic "{topic}" using the reference material below.

Reference Material:  
{context}

Questions:
"""
    response = model.generate_content(prompt)
    return response.text.strip().split("\n")


