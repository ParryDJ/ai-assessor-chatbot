import streamlit as st
import random
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="AI Assessor – Data Analyst L4", page_icon="📊", layout="wide")

# ---------- Theme & CSS ----------
st.markdown(
    """
    <style>
        body { background-color: #000000; color: #FFFFFF; }
        .stButton>button { background-color: #FFD500; color: #000000; font-weight: 600; border-radius: 8px; }
        textarea { border: 2px solid #FFD500 !important; border-radius: 8px !important; color: #000; background: #FFF9E6; }
        .question-box { background-color: #0f0f0f; padding: 12px; border-radius: 10px; border: 2px solid #FFD500; font-weight:700; color: #FFD500; }
        .sb-header { display:flex; align-items:center; gap:12px; }
        .logo { border-radius:8px; }
        .small-muted { color:#bfbfbf; font-size:0.9em; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
logo_url = "https://drive.google.com/uc?id=1F_wuHprzxMi8B9lSEm1gqApJUC083IX9"
col1, col2 = st.columns([1, 9])
with col1:
    try:
        st.image(logo_url, width=120)
    except Exception:
        st.write("")  # ignore if image load fails
with col2:
    st.title("📊 AI Assessor — Data Analyst (Level 4)")
    st.markdown("A conversational assessor that asks work-based questions against the apprenticeship KSBs. Theme: **Black & Yellow**")
    st.markdown("<div class='small-muted'>Questions rephrased to encourage workplace evidence. Responses can be exported as CSV.</div>", unsafe_allow_html=True)

# ---------- KSB bank (rewritten, 3-4 Qs each) ----------
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

# ---------- Sidebar: group and KSB selection ----------
st.sidebar.header("Assessment Controls")
group_options = list(ksb_bank.keys())
group = st.sidebar.selectbox("Select section", group_options)
ksb_list = list(ksb_bank[group].keys())
ksb_choice = st.sidebar.selectbox("Select KSB", ksb_list)

# Unique keys for session storage per KSB
ksb_key = f"{group}||{ksb_choice}"
qs_key = f"qs::{ksb_key}"
resp_key = f"resp::{ksb_key}"
step_key = f"step::{ksb_key}"
started_key = f"started::{ksb_key}"

# Initialize shuffled questions for this KSB if not already started or if KSB changed
if st.session_state.get(started_key) != ksb_choice:
    questions = ksb_bank[group][ksb_choice][:]
    random.shuffle(questions)
    st.session_state[qs_key] = questions
    st.session_state[resp_key] = [""] * len(questions)
    st.session_state[step_key] = 0
    st.session_state[started_key] = ksb_choice

questions = st.session_state[qs_key]
responses = st.session_state[resp_key]
step = st.session_state[step_key]

# ---------- Main UI: show question, text area, nav ----------
st.markdown(f"### {ksb_choice}")
st.markdown(f"<div class='small-muted'>Question order randomly set for this session — refresh the KSB to reshuffle.</div>", unsafe_allow_html=True)
st.write("")

if step < len(questions):
    q_text = questions[step]
    st.markdown(f"<div class='question-box'>Q{step + 1}: {q_text}</div>", unsafe_allow_html=True)
    response = st.text_area("Your answer (type here):", value=responses[step], key=f"ta_{qs_key}_{step}", height=200)

    nav_col1, nav_col2, nav_col3 = st.columns([1,1,6])
    with nav_col1:
        if st.button("Previous"):
            if step > 0:
                st.session_state[step_key] = step - 1
    with nav_col2:
        if st.button("Next"):
            if response.strip() == "":
                st.warning("Please enter a response before moving on.")
            else:
                # save response and advance
                st.session_state[resp_key][step] = response
                if step + 1 < len(questions):
                    st.session_state[step_key] = step + 1
                else:
                    st.session_state[step_key] = len(questions)  # mark complete
    with nav_col3:
        if st.button("Save & Exit"):
            st.session_state[resp_key][step] = response
            st.success("Progress saved. You can come back later and continue.")
else:
    st.success("✅ You have completed this KSB assessment!")
    # show summary table
    summary = pd.DataFrame({
        "KSB": [ksb_choice]*len(questions),
        "Question #": [i+1 for i in range(len(questions))],
        "Question": questions,
        "Response": responses
    })
    st.markdown("#### Your responses")
    st.dataframe(summary, height=300)

    # Download CSV
    csv_buffer = io.StringIO()
    summary.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode()
    download_label = f"Download responses ({ksb_choice}) — {datetime.utcnow().strftime('%Y%m%d_%H%MUTC')}.csv"
    st.download_button(label=download_label, data=csv_bytes, file_name=download_label, mime="text/csv")

    # Reset / restart options
    reset_col1, reset_col2 = st.columns([1,1])
    with reset_col1:
        if st.button("Restart this KSB"):
            random.shuffle(st.session_state[qs_key])
            st.session_state[resp_key] = [""] * len(st.session_state[qs_key])
            st.session_state[step_key] = 0
            st.experimental_rerun()
    with reset_col2:
        if st.button("Choose another KSB"):
            st.session_state[step_key] = 0
            # switching KSB in sidebar will re-init on next render

# ---------- Footer ----------
st.markdown("---")
st.markdown("Need changes? Ask me to alter wording, add more fields (e.g. evidence attachments), or connect responses to Google Sheets for central storage.")
