import streamlit as st
from ai_agent import AIAgent
import tempfile
import os

st.set_page_config(page_title="AI Document Chatbot", layout="wide")
st.title("📚 AI Document Chatbot")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for document upload
with st.sidebar:
    st.header("📖 Document Management")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    
    if uploaded_file is not None:
        st.write(f"✓ File: **{uploaded_file.name}**")
        st.write(f"Size: {uploaded_file.size / 1024:.1f} KB")
        
        if st.button("🔄 Process Document", key="process_btn", use_container_width=True):
            with st.spinner("⏳ Processing document..."):
                try:
                    # Validate file
                    if uploaded_file.size == 0:
                        st.error("❌ File is empty!")
                    elif uploaded_file.size > 50 * 1024 * 1024:  # 50MB limit
                        st.error("❌ File is too large (max 50MB)")
                    else:
                        # Save to temp file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=tempfile.gettempdir()) as tmp_file:
                            tmp_file.write(uploaded_file.getbuffer())
                            tmp_path = tmp_file.name
                        
                        st.info(f"📝 Temp file created: {tmp_path}")
                        
                        # Initialize agent with faster model
                        st.session_state.agent = AIAgent(model_name="orca-mini")
                        
                        # Load document
                        success = st.session_state.agent.load_document(tmp_path)
                        
                        if success:
                            st.session_state.document_loaded = True
                            st.session_state.chat_history = []
                            st.success("✅ Document loaded successfully!")
                        else:
                            st.error("❌ Failed to load document")
                        
                        # Cleanup
                        try:
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)
                        except:
                            pass
                        
                except Exception as e:
                    import traceback
                    st.error(f"❌ Error: {str(e)}")
                    st.error(f"Details: {traceback.format_exc()}")

# Main content area
if not st.session_state.document_loaded:
    st.info("👈 Upload a PDF document to get started")
else:
    # Display document summary
    with st.expander("📄 Document Info", expanded=False):
        st.write("Document loaded and ready for Q&A")
    
    # Chat interface
    st.subheader("💬 Ask Questions")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(answer)
    
    # Question input
    question = st.text_input(
        "Enter your question:",
        placeholder="What is the main topic of this document?",
        key="question_input"
    )
    
    if question:
        with st.spinner("🔍 Finding answer..."):
            try:
                answer = st.session_state.agent.answer_question(question)
                
                # Add to chat history
                st.session_state.chat_history.append((question, answer))
                
                # Display answer
                with st.chat_message("assistant"):
                    st.write(answer)
                    
            except Exception as e:
                st.error(f"❌ Error generating answer: {str(e)}")
