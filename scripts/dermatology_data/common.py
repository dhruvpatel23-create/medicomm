def q(question, correct, distractors, explanation, clinical=False):
    return {
        "question": question.strip(),
        "correct": correct.strip(),
        "distractors": [d.strip() for d in distractors],
        "explanation": explanation.strip(),
        "clinical": clinical
    }
