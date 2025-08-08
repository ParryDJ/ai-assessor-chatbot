
import streamlit as st
import random

# Define questions for each KSB
ksb_questions = {
    "K1: Legislation & Safe Use of Data": [
        "Can you explain at least one piece of legislation relevant to your role (e.g. GDPR, DPA) and its key principles?",
        "How do you follow this legislation in your daily work? Provide an example.",
        "Why is it important to follow this legislation when handling data?",
        "(Distinction) What are the risks or consequences of not following this legislation?"
    ],
    "K2: Organisational Data Policies": [
        "What internal data policies or procedures do you follow in your organisation?",
        "Where can you access these policies, and how do they affect your day-to-day work?",
        "(Distinction) What are the potential consequences of not following internal policies?"
    ],
    "K5: Structured vs Unstructured Data": [
        "Can you explain the difference between structured and unstructured data?",
        "Which type of data do you work with most often?",
        "How does the structure of the data impact your analysis approach?"
    ]
    # Add more KSBs as needed
}

st.title("📊 AI Assessor – Data Analyst L4 Apprenticeship")
st.markdown("This chatbot simulates an assessor asking questions based on the Knowledge, Skills and Behaviours (KSBs) from the Portfolio & Evidence Guide.")

# User selects a KSB topic
selected_ksb = st.selectbox("Choose a KSB to be assessed on:", list(ksb_questions.keys()))

# Load questions
questions = ksb_questions[selected_ksb]

# Start session
if "step" not in st.session_state:
    st.session_state.step = 0

# Show current question
if st.session_state.step < len(questions):
    current_question = questions[st.session_state.step]
    st.markdown(f"**Q{st.session_state.step + 1}: {current_question}**")
    user_response = st.text_area("Your answer:", key=f"response_{st.session_state.step}")

    if st.button("Next"):
        if user_response.strip():
            st.session_state.step += 1
        else:
            st.warning("Please enter a response before proceeding.")
else:
    st.success("You've completed this KSB assessment!")
    if st.button("Restart"):
        st.session_state.step = 0
