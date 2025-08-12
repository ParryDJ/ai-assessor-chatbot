import streamlit as st
import random
import pandas as pd
import io
from datetime import datetime
import openai
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Assessor – Data Analyst L4", page_icon="📊", layout="wide")

# ---------- THEME & CSS ----------
st.markdown("""
<style>
    body { background-color: #000000; color: #FFFFFF; }
    .stButton>button { background-color: #FFD500; color: #000000; font-weight: 600; border-radius: 8px; }
    textarea { border: 2px solid #FFD500 !important; border-radius: 8px !important; color: #000; background: #FFF9E6; }
    .question-box { background-color: #0f0f0f; padding: 12px; border-radius: 10px; border: 2px solid #FFD500; font-weight:700; color: #FFD500; }
    .small-muted { color:#bfbfbf; font-size:0.9em; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
logo_path = os.path.join(os.path.dirname(__file__), "Picture1.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=120)
else:
    st.warning("Logo not found. Please ensure Picture1.png is in the same folder.")

st.title("📊 AI Assessor — Data Analyst (Level 4)")
st.markdown("Black & Yellow theme. Modes: **Assessment**, **Help**, and **Portfolio Guidance**.")

# ---------- LOAD API KEY ----------
openai.api_key = st.secrets.get("OPENAI_API_KEY", None)

# ---------- KSB QUESTION BANK ----------
ksb_bank = {
    "Knowledge": {
        "K1: Legislation & Safe Use of Data": [
            "Which laws influence how you handle data in your role? Give an example.",
            "Describe a situation where you applied that legislation.",
            "Why is it important to follow these rules?",
            "What could happen if they are ignored?"
        ]
    },
    "Skills": {
        "S5: Impact of UX & Domain Context": [
            "Describe how user experience influenced an analysis you produced.",
            "Give an example where you tailored outputs to your audience.",
            "Why does understanding the domain improve analysis?"
        ]
    },
    "Behaviours": {
        "B2: Initiative & Resourcefulness": [
            "Describe a time you took initiative to solve a problem.",
            "What was the outcome and what did you learn?"
        ]
    }
}

# ---------- MODE SELECTION ----------
mode = st.sidebar.radio("Select Mode", ["Assessment Mode", "Help Mode", "Portfolio Guidance"])

# ---------- ASSESSMENT MODE ----------
if mode == "Assessment Mode":
    group = st.sidebar.selectbox("Select section", list(ksb_bank.keys()))
    ksb_choice = st.sidebar.selectbox("Select KSB", list(ksb_bank[group].keys()))
    ksb_key = f"{group}||{ksb_choice}"

    if f"qs::{ksb_key}" not in st.session_state:
        questions = ksb_bank[group][ksb_choice][:]
        random.shuffle(questions)
        st.session_state[f"qs::{ksb_key}"] = questions
        st.session_state[f"resp::{ksb_key}"] = [""] * len(questions)
        st.session_state[f"step::{ksb_key}"] = 0

    questions = st.session_state[f"qs::{ksb_key}"]
    responses = st.session_state[f"resp::{ksb_key}"]
    step = st.session_state[f"step::{ksb_key}"]

    if step < len(questions):
        q_text = questions[step]
        st.markdown(f"<div class='question-box'>Q{step + 1}: {q_text}</div>", unsafe_allow_html=True)
        response = st.text_area("Your answer:", value=responses[step], height=200)
        col_prev, col_next = st.columns(2)
        if col_prev.button("Previous") and step > 0:
            st.session_state[f"step::{ksb_key}"] = step - 1
        if col_next.button("Next"):
            if response.strip():
                st.session_state[f"resp::{ksb_key}"][step] = response
                st.session_state[f"step::{ksb_key}"] = step + 1
            else:
                st.warning("Please enter a response before moving on.")
    else:
        st.success("✅ You have completed this KSB assessment!")
        summary = pd.DataFrame({
            "KSB": [ksb_choice]*len(questions),
            "Question": questions,
            "Response": responses
        })
        st.dataframe(summary)
        csv_buffer = io.StringIO()
        summary.to_csv(csv_buffer, index=False)
        st.download_button("Download responses", data=csv_buffer.getvalue(), file_name=f"{ksb_choice}_responses.csv")

# ---------- HELP MODE ----------
elif mode == "Help Mode":
    st.subheader("💬 Ask a question about data analytics concepts")
    if not openai.api_key:
        st.error("OpenAI API key not set in Streamlit secrets.")
    else:
        learner_q = st.text_input("Your question:")
        if st.button("Get Answer") and learner_q.strip():
            with st.spinner("Thinking..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a friendly data analytics tutor who explains concepts clearly."},
                            {"role": "user", "content": learner_q}
                        ]
                    )
                    st.write(response.choices[0].message["content"])
                except Exception as e:
                    st.error(f"Error: {e}")

# ---------- PORTFOLIO GUIDANCE ----------
elif mode == "Portfolio Guidance":
    st.subheader("📁 Get guidance for your portfolio evidence")
    if not openai.api_key:
        st.error("OpenAI API key not set in Streamlit secrets.")
    else:
        ksb_help = st.selectbox("Select KSB for guidance", [f"{g} - {k}" for g in ksb_bank for k in ksb_bank[g]])
        user_input = st.text_area("Add any context about your work:", height=150)
        if st.button("Get Guidance"):
            with st.spinner("Preparing guidance..."):
                try:
                    guidance_prompt = f"""You are an apprenticeship assessor.
Give guidance for the KSB: {ksb_help}.
Do not provide the actual answer. 
Instead, explain what types of evidence, examples, and reflection a learner could include in their portfolio for this KSB.
Learner context: {user_input}"""
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a formal apprenticeship assessor giving portfolio evidence guidance only."},
                            {"role": "user", "content": guidance_prompt}
                        ]
                    )
                    st.write(response.choices[0].message["content"])
                except Exception as e:
                    st.error(f"Error: {e}")
