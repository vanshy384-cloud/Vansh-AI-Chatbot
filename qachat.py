from dotenv import load_dotenv
import streamlit as st
import os
from google import genai

# Load API Key
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# Gemini Client
client = genai.Client(api_key=api_key)

# Streamlit Page
st.set_page_config(
    page_title="Vansh AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Vansh AI Chatbot")
st.write("Ask me anything!")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for role, message in st.session_state.messages:
    if role == "You":
        st.markdown(f"🧑 **You:** {message}")
    else:
        st.markdown(f"🤖 **Vansh AI:** {message}")

# Input
question = st.text_input("Enter your question")

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Thinking..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=question
                )

                answer = response.text

                st.session_state.messages.append(("You", question))
                st.session_state.messages.append(("Vansh AI", answer))

                st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")