import streamlit as st
import random
import pandas as pd
import io
from datetime import datetime
import openai
import os

st.set_page_config(page_title="Data Analyst L4 Bot", page_icon="", layout="wide")

# ---------- THEME ----------
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

st.title("Data Analyst (Level 4)")
st.markdown("Modes: **Assessment**, **Help**, and **Portfolio Guidance**.")

openai.api_key = st.secrets.get("OPENAI_API_KEY", None)

# ---------- KSB QUESTION BANK (Full) ----------
ksb_bank = {
    "Knowledge": {
        "K1: Legislation & Safe Use of Data": [
            "Which laws, regulations or official standards influence how you handle data in your role? Tell me one example and its key points.",
            "Describe a situation at work where you applied that rule — what did you do and why?",
            "Why is adherence to that legislation important for your team or organisation?",
            "What might happen if those legal requirements were not followed?"
        ],
        "K2: Organisational Data Policies": [
            "What internal data policies or procedures are most relevant to your day-to-day work?",
            "Where do you find those policies and how do they shape what you do?",
            "Give a concrete example of how you followed (or enforced) an internal policy.",
            "What issues could arise if staff ignored these internal rules?"
        ],
        "K5: Structured vs Unstructured Data": [
            "How would you explain structured versus unstructured data to a colleague?",
            "Which data formats do you work with most, and where do you see the other kinds used in your organisation?",
            "How does the data’s structure change the way you analyse it?",
            "What challenges have you faced when dealing with unstructured data (if any)?"
        ],
        "K6: Data Structures & Database Design": [
            "Name three data structures (files, tables, arrays, records, trees, etc.) you use and briefly explain each.",
            "What database architecture is used where you work (e.g. relational, cloud-based, hybrid)?",
            "How is your database implemented and who manages access rights/security?",
            "How are backups and maintenance handled — and what happens if capacity limits are reached?"
        ],
        "K7: UX & Domain Context for Analytics": [
            "Why does user experience matter when you present data or insights?",
            "Describe how you tailor outputs to the audience or domain you’re working in.",
            "Give an example where domain knowledge changed how you interpreted data.",
            "How do you ensure your work avoids misleading stakeholders?"
        ],
        "K10: Combining Data from Different Sources": [
            "What approaches do you use to bring together data from different sources?",
            "Tell me about a case where combining datasets improved an analysis or decision.",
            "What checks or safeguards do you use to reduce risks when merging data?",
            "What are the main pitfalls to watch for when joining multiple sources?"
        ],
        "K13: Principles of Statistics": [
            "Which statistical methods do you apply in your analyses (e.g. mean, correlation, hypothesis testing)?",
            "Explain the difference between descriptive and inferential statistics in plain terms.",
            "Describe a workplace example where statistics helped you draw a meaningful conclusion.",
            "What assumptions or limitations did you consider when using the method?"
        ],
        "K14: Descriptive, Predictive & Prescriptive Analytics": [
            "How do you distinguish descriptive, predictive and prescriptive analytics in practice?",
            "Give an example from your role where you used each type (or where you would).",
            "What are the benefits of using predictive models for your organisation?",
            "What risks or biases do you watch for in predictive analytics?"
        ],
        "K15: Ethics in Data Collection & Use": [
            "What ethical issues do you consider when gathering data (consent, bias, minimisation)?",
            "Describe steps you take to ensure ethical use of data in a real task.",
            "Why is ethical practice important for trust and decision-making in your organisation?",
            "Give an example where you changed an approach because of an ethical concern."
        ]
    },
    "Skills": {
        "S5: Impact of UX & Domain Context": [
            "Describe how user experience influenced an analysis you produced.",
            "Share a real example where you adjusted communication to meet stakeholder needs.",
            "What choices did you make to improve the clarity and usefulness of the insight?",
            "How did feedback or domain constraints change the final output?"
        ],
        "S9: Apply Organisational Architecture Requirements": [
            "What tools and techniques do you use to work within your organisation’s architecture?",
            "Explain how you export, share or restrict data to meet internal standards.",
            "How does this process align with data security and compliance in your workplace?",
            "Describe a time you adapted your process to comply with architectural rules."
        ],
        "S10: Apply Statistical Methodologies": [
            "Which specific statistical methods have you applied at work (list examples)?",
            "For one example, explain how you applied it and what insight it gave you.",
            "How did that result influence a decision or action in the business?",
            "What steps did you take to validate the statistical approach?"
        ],
        "S11: Apply Predictive Analytics": [
            "Describe a predictive analytics project you were involved in (e.g. forecasting, regression).",
            "Outline the process you followed from data prep to model evaluation and interpretation.",
            "What insights did the model deliver and how were they used?",
            "What controls did you use to check for accuracy, bias or overfitting?"
        ],
        "S13: Analytical Techniques (Mining, Forecasting, Modelling)": [
            "Describe three analytical techniques you’ve used (e.g. clustering, time-series forecasting, regression).",
            "For each technique, explain the process and the insight it produced.",
            "How did those insights lead to business improvements or decisions?",
            "What limitations or validation steps did you consider for each technique?"
        ],
        "S14: Collate & Visualise Qual + Quant Data": [
            "Give three examples of how you turned data into visuals or reports for different audiences.",
            "Why did you choose each visualisation style, and how did it aid understanding?",
            "Explain how you adapted visuals to the stakeholder’s domain knowledge.",
            "How did you check the visuals were accessible and not misleading?"
        ]
    },
    "Behaviours": {
        "B1: Productive, Professional & Secure Environment": [
            "How do you help maintain a secure and productive environment when working with data?",
            "Which laws or internal practices inform how you behave with data day-to-day?",
            "Give an example where you applied these practices in a project.",
            "What would be the consequences of not following these practices?"
        ],
        "B2: Initiative & Resourcefulness": [
            "Describe a time you took initiative to solve a problem in your remit.",
            "What steps did you take and how did you decide on that course of action?",
            "What was the outcome and what did you learn from it?",
            "How did you make sure your solution was sustainable?"
        ],
        "B5: Root Cause Analysis & Problem Solving": [
            "Tell me about a complex issue you investigated and how you identified the root cause.",
            "What techniques or tools did you use to dig deeper into the problem?",
            "What permanent fix did you apply to prevent recurrence?",
            "How did you validate that the solution worked?"
        ],
        "B6: Resilience & Learning from Failure": [
            "Describe an instance where something went wrong and how you responded.",
            "What changes did you make afterwards to reduce future risk?",
            "What did you learn personally from the experience?",
            "How have you applied those lessons in later work?"
        ],
        "B7: Adapting to Changing Contexts": [
            "Give an example where project context or stakeholder needs changed and you adapted.",
            "What did you change in your approach and why?",
            "How did this adaptation support the project’s goals?",
            "What would you do differently next time?"
        ]
    }
}


mode = st.sidebar.radio("Select Mode", ["Assessment Mode", "Help Mode", "Portfolio Guidance"])

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
                    guidance_prompt = f"You are an apprenticeship assessor. Give guidance for the KSB: {ksb_help}. Do not provide the actual answer. Instead, explain what types of evidence, examples, and reflection a learner could include in their portfolio for this KSB. Learner context: {user_input}"
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
