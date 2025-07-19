import streamlit as st
import sys
import os

# Add the src directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.orchestrator import answer_question
from src.app_config import config
from src.langchain_setup import init_system

st.title("Movie Knowledge Chatbot 🎬 ")

# Initialize Swarm Memory in session state
if "swarm_memory" not in st.session_state:
    st.session_state.swarm_memory = init_system()

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field for user to ask a question
user_input = st.text_input("Ask a movie question:")

# Button to submit the question
if st.button("Ask") and user_input.strip():
    # Get answer from orchestrator
    answer = answer_question(
        user_input,
        config,
        st.session_state.swarm_memory
    )
    # Log answer in memory
    st.session_state.swarm_memory.log_answer(user_input, answer)
    # Add to chat history
    st.session_state.chat_history.append({"question": user_input, "answer": answer})

# Button to clear chat history
if st.button("Clear History"):
    st.session_state.chat_history = []

# Display chat history with the newest messages on top
st.markdown("### Conversation History")
for entry in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {entry['question']}")
    st.markdown(f"**Bot:**\n {entry['answer']}")
    st.markdown("---")
