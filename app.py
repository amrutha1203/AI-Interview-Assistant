import streamlit as st
import pdfplumber
from docx import Document
import os

st.set_page_config(
    page_title="AI Interview Assistant",
    layout="centered"
)

# ---------------- SESSION STATE ----------------

if "questions" not in st.session_state:
    st.session_state.questions = [
        "Tell me about yourself.",
        "What are your strengths?",
        "What are your weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?"
    ]

if "index" not in st.session_state:
    st.session_state.index = 0

if "started" not in st.session_state:
    st.session_state.started = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------- SCORING FUNCTION ----------------

def evaluate(answer):
    answer = answer.lower()

    score = 0

    if len(answer) > 30:
        score += 2

    if "team" in answer:
        score += 1

    if "learn" in answer:
        score += 1

    if "improve" in answer:
        score += 1

    return min(score, 5)

# ---------------- FILE EXTRACTION ----------------

def extract_text(file):
    extension = os.path.splitext(file.name)[1].lower()

    try:
        if extension == ".pdf":
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text

        elif extension == ".docx":
            doc = Document(file)
            return "\n".join(para.text for para in doc.paragraphs)

        elif extension == ".txt":
            return file.read().decode("utf-8")

        else:
            return "Unsupported file type."

    except Exception as e:
        return f"Error reading file: {e}"

# ---------------- UI ----------------

st.title("🤖 AI Interview Assistant")

# ---------------- START SCREEN ----------------

if not st.session_state.started:

    name = st.text_input("Enter your name")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    if resume is not None:
        st.session_state.resume_text = extract_text(resume)
        st.success("Resume uploaded successfully ✔")

    if st.button("Start Interview"):

        if name.strip():

            st.session_state.name = name
            st.session_state.started = True
            st.rerun()

        else:
            st.warning("Please enter your name.")

# ---------------- INTERVIEW SCREEN ----------------

else:

    st.subheader(f"Candidate: {st.session_state.name}")

    if st.session_state.resume_text:

        with st.expander("View Resume Text"):
            st.write(st.session_state.resume_text[:2000])

    i = st.session_state.index
    questions = st.session_state.questions

    if i < len(questions):

        st.write(f"### Question {i + 1}")
        st.write(questions[i])

        answer = st.text_area(
            "Your Answer",
            key=f"answer_{i}"
        )

        if st.button("Submit Answer"):

            if answer.strip():

                st.session_state.answers.append(answer)
                st.session_state.index += 1

                st.rerun()

            else:
                st.warning("Please enter your answer.")

    else:

        total_score = 0

        for answer in st.session_state.answers:
            total_score += evaluate(answer)

        max_score = len(st.session_state.questions) * 5

        st.success("Interview Completed 🎉")

        st.write(f"### Final Score: {total_score} / {max_score}")

        st.subheader("Your Answers")

        for i, answer in enumerate(st.session_state.answers):
            st.write(f"**Q{i+1}: {st.session_state.questions[i]}**")
            st.write(answer)

            answer_score = evaluate(answer)
            st.write(f"Score: {answer_score}/5")
            st.divider()

        if total_score >= 18:
            st.success("Excellent Performance ⭐")
            st.balloons()

        elif total_score >= 12:
            st.info("Good Performance 👍")

        else:
            st.warning("Needs Improvement 📌")

        if st.button("Restart Interview"):

            st.session_state.index = 0
            st.session_state.started = False
            st.session_state.name = ""
            st.session_state.resume_text = ""
            st.session_state.answers = []

            st.rerun()