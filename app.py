""" import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


# Set your OpenAI API key (or use environment variable for security)
import os
os.environ["OPENAI_API_KEY"] = "05eaba6dd95047d4bb17657d26f71cac"  # replace with your key

# Initialize LLM (can change to another like ChatOpenAI, GPT4All, etc.)
llm = OpenAI(temperature=0.7)

# Streamlit UI
st.title("📚 Learning Buddy - Quiz Generator")

# User inputs
topic = st.selectbox("Select a Math Topic", ["Algebra", "Calculus", "Trigonometry", "Geometry", "Statistics"])
difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
num_questions = st.slider("Number of Questions", min_value=1, max_value=20, value=5)

# Button to trigger generation
if st.button("Generate Quiz"):
    with st.spinner("Generating questions..."):
        # Prompt template
        template =
       # You are a smart AI tutor. Generate {num} {difficulty} level multiple choice math questions on the topic of {topic}.
        #Include the correct answer and a short explanation for each.
        
        prompt_text = template.format(num=num_questions, difficulty=difficulty.lower(), topic=topic)

        
        
        llm = ChatOpenAI(
        temperature=0.7,
        openai_api_base="https://api.aimlapi.com/v1",
        openai_api_key="05eaba6dd95047d4bb17657d26f71cac",
        model_name="gpt-3.5-turbo"
        )
        # Later inside your button logic
        response = llm([HumanMessage(content=prompt_text)])
        st.write(response.content)
"""

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
import json

# Set AIMLAPI key and base
os.environ["OPENAI_API_KEY"] = "05eaba6dd95047d4bb17657d26f71cac"
API_BASE = "https://api.aimlapi.com/v1"

# Initialize LLM
llm = ChatOpenAI(
    temperature=0.7,
    openai_api_base=API_BASE,
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model_name="gpt-3.5-turbo"
)

st.title("📚 Learning Buddy - Quiz Generator")

# Step 1: Inputs
topic = st.selectbox("Select a Math Topic", ["Algebra", "Calculus", "Trigonometry", "Geometry", "Statistics"])
difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=3)

# Session state to store quiz
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "show_answers" not in st.session_state:
    st.session_state.show_answers = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# Step 2: Generate Quiz
if st.button("Generate Quiz"):
    st.session_state.show_answers = False
    st.session_state.user_answers = {}

    with st.spinner("Generating questions..."):
        prompt = f"""
        You are a smart AI tutor. Generate {num_questions} {difficulty.lower()} level multiple choice math questions on the topic of {topic}.
        Format output as JSON in this structure:
        [
            {{
                "question": "...",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "explanation": "..."
            }},
            ...
        ]
        """
        response = llm([HumanMessage(content=prompt)])
        try:
            st.session_state.quiz_data = json.loads(response.content)
        except:
            st.error("Failed to parse questions. Please try again.")

# Step 3: Show Questions
if st.session_state.quiz_data:
    st.subheader("📝 Quiz Time!")

    for idx, item in enumerate(st.session_state.quiz_data):
        st.write(f"**Q{idx+1}: {item['question']}**")
        st.session_state.user_answers[idx] = st.radio(
            f"Choose your answer (Q{idx+1})",
            item['options'],
            key=f"q_{idx}"
        )
        st.markdown("---")

    if st.button("Submit Answers"):
        st.session_state.show_answers = True

# Step 4: Show Answers
if st.session_state.show_answers:
    st.subheader("✅ Results")
    for idx, item in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers[idx]
        correct = item["correct_answer"]
        explanation = item["explanation"]
        is_correct = "✅ Correct!" if user_ans == correct else "❌ Incorrect"

        with st.expander(f"Q{idx+1} Answer & Explanation"):
            st.write(f"**Your Answer:** {user_ans}")
            st.write(f"**Correct Answer:** {correct}")
            st.write(f"**Result:** {is_correct}")
            st.write(f"**Explanation:** {explanation}")
