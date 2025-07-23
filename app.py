import streamlit as st
from pdf_utils import convert_pdf_to_images
from detector import process_answer_sheet
from scorer import score_answers
import pandas as pd

st.title("📄 Answer Sheet Scoring System (Multi-Answer Support)")

# 1. Input answer key
st.subheader("Step 1: Input Answer Key")
num_questions = 120
answer_key = {}
with st.form("answer_key_form"):
    cols = st.columns(6)
    for i in range(1, num_questions + 1):
        col = cols[(i - 1) % 6]
        answer = col.multiselect(f"Q{i}", ["A", "B", "C", "D", "E"], key=f"q{i}")
        if answer:
            answer_key[i] = answer
    submitted = st.form_submit_button("Submit Answer Key")

# 2. Upload PDF
st.subheader("Step 2: Upload Answer Sheet PDF")
uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])

# 3. Process and Score
if uploaded_pdf and submitted and st.button("Process & Score"):
    images = convert_pdf_to_images(uploaded_pdf)
    results = []

    for i, img in enumerate(images):
        student_id, answers = process_answer_sheet(img)
        score, per_question = score_answers(answers, answer_key)
        results.append({
            "Student ID": student_id,
            **per_question,
            "Total Score": score
        })

    df = pd.DataFrame(results)
    st.subheader("📊 Results")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode()
    st.download_button("Download CSV", csv, "scores.csv", "text/csv")