def score_answers(student_answers, answer_key):
    score = 0
    per_question = {}
    for q, correct_ans in answer_key.items():
        marked = student_answers.get(q)
        per_question[f"Q{q}"] = marked
        if marked == correct_ans:
            score += 1
    return score, per_question