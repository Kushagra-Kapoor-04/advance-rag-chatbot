import os
import streamlit as st
from dotenv import load_dotenv
from rag_pipeline import build_qa_chain
from datetime import datetime
import json

load_dotenv()

UPLOAD_DIR = "data/uploads"
HISTORY_FILE = "data/chat_history.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

st.set_page_config(page_title="Advanced RAG Chatbot", layout="wide")
st.title("📚 Advanced PDF Chatbot (RAG)")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load chat history from file
def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

# Save chat history to file
def save_chat_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Load history at startup
if not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history()

# Sidebar
st.sidebar.header("Model Settings")

llm_provider = "Gemini"  # Using Gemini only

answer_style = st.sidebar.selectbox(
    "Answer Style",
    [
        "Short and concise",
        "Detailed explanation",
        "Exam-oriented with examples",
        "Bullet points",
        "Teach me like a beginner"
    ]
)

# Chat History Section
with st.sidebar.expander("📜 Chat History", expanded=False):
    if st.session_state.chat_history:
        for i, item in enumerate(reversed(st.session_state.chat_history)):
            st.write(f"**Q {len(st.session_state.chat_history) - i}:** {item['question'][:50]}...")
            st.write(f"**A:** {item['answer'][:100]}...")
            st.divider()
        
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            save_chat_history([])
            st.success("Chat history cleared!")
            st.rerun()
    else:
        st.write("No chat history yet. Start asking questions!")

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    file_paths = []
    for file in uploaded_files:
        path = os.path.join(UPLOAD_DIR, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        file_paths.append(path)

    st.success("PDFs uploaded and ready")

    query = st.text_input("Ask a question")

    if query:
        with st.spinner("Thinking..."):
            qa_chain = build_qa_chain(
                file_paths,
                answer_style,
                llm_provider
            )

            response = qa_chain.invoke({"input": query})

        st.subheader("Answer")
        st.write(response["output_text"])

        # Save to chat history
        history_item = {
            "timestamp": datetime.now().isoformat(),
            "question": query,
            "answer": response["output_text"],
            "answer_style": answer_style,
            "sources": [doc.metadata.get('source', 'Unknown') for doc in response["source_documents"]]
        }
        st.session_state.chat_history.append(history_item)
        save_chat_history(st.session_state.chat_history)

        with st.expander("📄 Source Documents"):
            for doc in response["source_documents"]:
                st.write(
                    f"{doc.metadata.get('source')} | Page {doc.metadata.get('page')}"
                )

# Show full chat history at bottom
if st.session_state.chat_history:
    st.divider()
    st.subheader("📚 Full Conversation History")
    
    for i, item in enumerate(st.session_state.chat_history, 1):
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.write(f"**Q {i}:**")
        with col2:
            st.write(item['question'])
        
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.write(f"**A {i}:**")
        with col2:
            st.write(item['answer'])
        
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.write(f"**Style:**")
        with col2:
            st.write(f"`{item['answer_style']}`")
        
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.write(f"**Time:**")
        with col2:
            st.write(f"`{item['timestamp']}`")
        
        st.divider()

