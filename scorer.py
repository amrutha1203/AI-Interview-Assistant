import re

def evaluate(question, answer):

    if not answer.strip():
        return 0, "No answer provided."

    score = 6  # base strict score

    length = len(answer)

    # STRICT RULES
    if length < 30:
        score -= 2
    if length > 200:
        score += 1
    if "I don't know" in answer.lower():
        score -= 3
    if "example" in answer.lower():
        score += 1

    score = max(0, min(10, score))

    feedback = "Needs improvement in clarity and depth."

    if score >= 8:
        feedback = "Strong answer with good clarity."
    elif score >= 6:
        feedback = "Average answer. Add examples."
    else:
        feedback = "Weak answer. Needs preparation."

    return score, feedback