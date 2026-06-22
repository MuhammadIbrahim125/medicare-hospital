import streamlit as st
from openai import OpenAI
import os

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Grok Tutor",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("📚 Grok AI Tutor")
st.caption("Your personal intelligent tutor — ask anything!")

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("xAI API Key", type="password", value=os.getenv("XAI_API_KEY", ""))
    if not api_key:
        st.warning("Please enter your xAI API key")
        st.info("Get it at: https://x.ai/api")
    
    model = st.selectbox("Model", ["grok-4", "grok-3"], index=0)
    
    st.divider()
    st.markdown("**Tutor Mode**")
    subject = st.selectbox("Focus Area", [
        "General Tutor", "Physics", "Mathematics", "Computer Science", 
        "Biology", "Chemistry", "History", "Literature"
    ])
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ===================== CLIENT =====================
@st.cache_resource
def get_client(api_key):
    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

if api_key:
    client = get_client(api_key)
else:
    client = None

# ===================== CHAT HISTORY =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"""You are Grok, a world-class AI Tutor built by xAI.
        You are helpful, patient, and encouraging. 
        Explain concepts clearly with examples. 
        Ask follow-up questions to check understanding.
        Current focus: {subject}"""}
    ]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ===================== USER INPUT =====================
if prompt := st.chat_input("Ask me anything... (e.g., Explain quantum entanglement)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not client:
            st.error("Please add your xAI API key in the sidebar.")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=st.session_state.messages,
                        temperature=0.7,
                        max_tokens=2048,
                        stream=False
                    )
                    answer = response.choices[0].message.content
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ===================== FOOTER =====================
st.caption("Built with using Streamlit + Grok by xAI")