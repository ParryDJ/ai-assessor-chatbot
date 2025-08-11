import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# The core KSB knowledge base (simplified for demo, use full text in practice)
KSB_KNOWLEDGE = """
K1: current relevant legislation and its application to safe use of data - DPA, GDPR, importance of compliance.
K2: organisational data policies and procedures - internal policies on data privacy, protection, retention.
K5: differences between structured and unstructured data.
K6: fundamentals of data structures and database design - files, lists, arrays, relational DBs.
K7: principles of user experience and domain context in data analytics.
K10: approaches to combining data from different sources, benefits, and risks.
K13: principles of statistics for data analysis - descriptive and inferential stats.
K14: principles of descriptive, predictive, and prescriptive analytics - definitions, applications, risks.
K15: ethical aspects in data collation and use - consent, bias, transparency, anonymisation.
S5: impact of user experience on data analysis communication.
S9: organisational architecture requirements in data handling.
S10: applying statistics in data tasks.
S11: applying predictive analytics - time series, regression, risks and benefits.
S13: analytical techniques - data mining, time series forecasting, modelling.
S14: presenting data analysis in visual formats - dashboards, reports, infographics.
B1-B7: professional working environment, initiative, problem-solving, resilience, adaptability.
"""

# Template prompt for asking questions based on KSB topic
def generate_question_prompt(topic_code):
    prompt = f"""
You are an expert assessor for the Level 4 Data Analyst Apprenticeship.
Using the KSB knowledge provided below, generate a challenging but fair question for the learner to answer about {topic_code}.
KSB summary:
{KSB_KNOWLEDGE}

Question:
"""
    return prompt.strip()

# Function to ask the bot to generate a question about a specific KSB topic
def ask_question(topic_code):
    prompt = generate_question_prompt(topic_code)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful apprenticeship assessor AI."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Template prompt for answering learner's help questions about the KSBs
def generate_help_prompt(user_question):
    prompt = f"""
You are an expert AI tutor specialized in the Level 4 Data Analyst Apprenticeship, focusing on the KSBs (Knowledge, Skills, Behaviours) for the Portfolio & Evidence Guide.
Answer the learner's question below as clearly and informatively as possible, referencing the KSBs knowledge base when relevant.

KSB summary:
{KSB_KNOWLEDGE}

Learner question:
{user_question}

Answer:
"""
    return prompt.strip()

# Function to answer freeform learner questions about the KSBs
def help_center_answer(user_question):
    prompt = generate_help_prompt(user_question)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful apprenticeship help center AI."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

# Simple CLI chatbot example
def chatbot():
    print("Welcome to the Data Academy L4 Apprenticeship AI Chatbot!")
    print("Type 'question <KSB_code>' to get a question (e.g. question K1).")
    print("Type 'help <your question>' to ask anything about the KSBs.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower().startswith("question"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                ksb_code = parts[1].strip().upper()
                print(f"\nAI Question on {ksb_code}:")
                try:
                    question = ask_question(ksb_code)
                    print(question)
                except Exception as e:
                    print(f"Error generating question: {e}")
            else:
                print("Please specify a KSB code after 'question'.")
        elif user_input.lower().startswith("help"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                learner_question = parts[1].strip()
                print("\nAI Help Center Answer:")
                try:
                    answer = help_center_answer(learner_question)
                    print(answer)
                except Exception as e:
                    print(f"Error generating answer: {e}")
            else:
                print("Please type your question after 'help'.")
        else:
            print("Unknown command. Use 'question <KSB_code>' or 'help <your question>' or 'exit'.")

if __name__ == "__main__":
    chatbot()
