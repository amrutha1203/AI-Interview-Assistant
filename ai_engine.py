from PyPDF2 import PdfReader
import random

def read_resume(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8")


def generate_questions(resume_text):

    skills = ["Python", "Java", "C", "AI", "ML", "SQL", "DSA", "HTML"]

    found = [s for s in skills if s.lower() in resume_text.lower()]

    questions = [
        "Introduce yourself in 1 minute.",
        "Explain your strongest project.",
        "Why should we hire you?",
        "What are your weaknesses?",
        "Explain a challenging situation you solved."
    ]

    # skill-based questions
    for s in found:
        questions.append(f"Explain your experience with {s} in detail.")

    random.shuffle(questions)

    return questions[:6]