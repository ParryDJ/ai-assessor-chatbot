# ai_assessor_chatbot_all_ksbs.py
import streamlit as st
import random
import pandas as pd
import io
import openai

st.set_page_config(page_title="AI Assessor – Data Analyst L4", page_icon="📊", layout="wide")

openai.api_key = st.secrets.get("OPENAI_API_KEY", None)

st.markdown(
    """
    <style>
        body { background-color: #000000; color: #FFFFFF; }
        .stButton>button { background-color: #FFD500; color: #000000; font-weight: 600; border-radius: 8px; }
        textarea { border: 2px solid #FFD500 !important; border-radius: 8px !important; color: #000; background: #FFF9E6; }
        .question-box { background-color: #0f0f0f; padding: 12px; border-radius: 10px; border: 2px solid #FFD500; font-weight:700; color: #FFD500; }
        .small-muted { color:#bfbfbf; font-size:0.9em; }
    </style>
    """, unsafe_allow_html=True
)

col1, col2 = st.columns([1, 9])
with col1:
    st.image("logo_placeholder.png", width=120)
with col2:
    st.title("📊 AI Assessor — Data Analyst (Level 4)")
    st.markdown("A conversational assessor that asks work-based questions against the apprenticeship KSBs **and** answers learner questions.")
    st.markdown("<div class='small-muted'>Assessment Mode → asks KSB questions. Help Mode → answers learner questions via OpenAI.</div>", unsafe_allow_html=True)

ksb_bank = {
    "Knowledge": {
        "K1: Legislation & Safe Use of Data": [
            "Which laws influence how you handle data?",
            "Describe a situation where you applied that rule.",
            "Why is it important to follow that legislation?",
            "What could happen if these rules are ignored?"
        ]
    },
    "Skills": {
        "S5: Impact of UX & Domain Context": [
            "Describe how user experience influenced an analysis you produced.",
            "Share an example where you adjusted communication to meet stakeholder needs.",
            "Why does understanding the domain context improve your analysis?"
        ]
    },
    "Behaviours": {
        "B2: Initiative & Resourcefulness": [
            "Describe a time you took initiative to solve a problem.",
            "What was the outcome and what did you learn from it?",
            "How did your actions benefit the project or team?"
        ]
    }
}

mode = st.sidebar.radio("Select Mode", ["Assessment Mode", "Help Mode"])

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

elif mode == "Help Mode":
    st.subheader("💬 Ask a question about data analytics concepts")
    if openai.api_key is None:
        st.error("OpenAI API key not set. Please add it to Streamlit secrets.")
    else:
        learner_q = st.text_input("Type your question:")
        if st.button("Get Answer") and learner_q.strip():
            with st.spinner("Thinking..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a friendly data analytics tutor who explains clearly without giving portfolio answers."},
                            {"role": "user", "content": learner_q}
                        ]
                    )
                    st.write(response.choices[0].message["content"])
                except Exception as e:
                    st.error(f"Error: {e}")
