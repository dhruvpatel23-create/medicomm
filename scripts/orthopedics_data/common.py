def q(prompt, answer, wrong, explanation, clinical=True, difficulty="high"):
    prompt = prompt.strip()
    if prompt and prompt[-1] not in ".?!:":
        prompt = f"{prompt}:"
    options = [answer, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(f"Options must be 4 unique strings. Got: {options} for prompt: {prompt[:40]}")
    return {
        "prompt": prompt,
        "options": options,
        "answerIndex": 0,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["clinical"] if clinical else ["hard-recall"],
    }
