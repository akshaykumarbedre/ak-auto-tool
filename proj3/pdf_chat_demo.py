"""
PDF Chat App - Simplified Demo Version

This is a demonstration version that shows the complete structure
and functionality of the PDF chat application, designed to work
even if some dependencies are not available.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Streamlit
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("⚠️  Streamlit not available. This is a demo version.")

# Try to import LlamaIndex components
try:
    from llama_index.core import VectorStoreIndex, StorageContext
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.core.memory import ChatMemoryBuffer
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False
    print("⚠️  LlamaIndex not available in demo mode.")

# Try to import readers
try:
    from llama_index.readers.file import PyMuPDFReader
    PYMUPDF_READER_AVAILABLE = True
except ImportError:
    PYMUPDF_READER_AVAILABLE = False
    print("⚠️  PyMuPDFReader not available in demo mode.")

try:
    import pymupdf
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("⚠️  PyMuPDF not available in demo mode.")

# Mock classes for demo purposes
class MockDocument:
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

class MockIndex:
    def __init__(self, documents):
        self.documents = documents
    
    def as_chat_engine(self, **kwargs):
        return MockChatEngine(self.documents)

class MockChatEngine:
    def __init__(self, documents):
        self.documents = documents
    
    def chat(self, message):
        # Simple mock response
        return f"Mock response to: {message}. This would normally search through {len(self.documents)} documents."

class PDFChatApp:
    def __init__(self):
        self.index = None
        self.chat_engine = None
        if STREAMLIT_AVAILABLE:
            self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if "documents_processed" not in st.session_state:
            st.session_state.documents_processed = False
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "index" not in st.session_state:
            st.session_state.index = None
        if "chat_engine" not in st.session_state:
            st.session_state.chat_engine = None
    
    def load_environment_variables(self):
        """Load environment variables from .env file"""
        env_path = Path(__file__).parent / "notebook" / ".env"
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"')
                            os.environ[key] = value
    
    def process_pdfs_quick_parse(self, uploaded_files: List[Any]) -> List[Any]:
        """Process PDFs using PyMuPDFReader (quick parse) or mock"""
        documents = []
        
        if PYMUPDF_READER_AVAILABLE:
            reader = PyMuPDFReader()
            
            with tempfile.TemporaryDirectory() as temp_dir:
                for uploaded_file in uploaded_files:
                    # Save uploaded file to temporary directory
                    file_path = Path(temp_dir) / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Read PDF
                    try:
                        docs = reader.load_data(file_path)
                        documents.extend(docs)
                        if STREAMLIT_AVAILABLE:
                            st.success(f"✅ Quick parse completed for {uploaded_file.name}")
                    except Exception as e:
                        if STREAMLIT_AVAILABLE:
                            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        else:
            # Mock processing
            for uploaded_file in uploaded_files:
                mock_doc = MockDocument(
                    f"Mock content from {uploaded_file.name}",
                    {"filename": uploaded_file.name}
                )
                documents.append(mock_doc)
                if STREAMLIT_AVAILABLE:
                    st.success(f"✅ Mock quick parse completed for {uploaded_file.name}")
        
        return documents
    
    def process_pdfs_llama_parse(self, uploaded_files: List[Any]) -> List[Any]:
        """Process PDFs using LlamaParse (detailed parse) or fallback to quick parse"""
        try:
            from llama_cloud import LlamaCloudReader
            
            reader = LlamaCloudReader(
                result_type="markdown",
                verbose=True
            )
            
            documents = []
            with tempfile.TemporaryDirectory() as temp_dir:
                file_paths = []
                for uploaded_file in uploaded_files:
                    file_path = Path(temp_dir) / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    file_paths.append(str(file_path))
                
                # Parse all files
                docs = reader.load_data(file_paths)
                documents.extend(docs)
                
                for uploaded_file in uploaded_files:
                    if STREAMLIT_AVAILABLE:
                        st.success(f"✅ Detailed parse completed for {uploaded_file.name}")
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"❌ Error with LlamaParse: {str(e)}")
                st.info("💡 Falling back to quick parse...")
            return self.process_pdfs_quick_parse(uploaded_files)
        
        return documents
    
    def create_index(self, documents: List[Any]):
        """Create vector index from documents"""
        try:
            if LLAMA_INDEX_AVAILABLE:
                # Real implementation
                node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
                storage_context = StorageContext.from_defaults()
                
                index = VectorStoreIndex.from_documents(
                    documents,
                    storage_context=storage_context,
                    node_parser=node_parser,
                    show_progress=True
                )
                
                return index
            else:
                # Mock implementation
                return MockIndex(documents)
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"❌ Error creating index: {str(e)}")
            return None
    
    def create_chat_engine(self, index):
        """Create chat engine from index"""
        try:
            if LLAMA_INDEX_AVAILABLE:
                # Real implementation
                memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
                
                chat_engine = index.as_chat_engine(
                    memory=memory,
                    system_prompt=(
                        "You are a helpful assistant that answers questions based on the provided PDF documents. "
                        "Use the context from the documents to provide accurate and detailed responses. "
                        "If you cannot find relevant information in the documents, please say so."
                    ),
                    verbose=True
                )
                
                return chat_engine
            else:
                # Mock implementation
                return MockChatEngine(index.documents if hasattr(index, 'documents') else [])
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"❌ Error creating chat engine: {str(e)}")
            return None
    
    def render_sidebar(self):
        """Render the sidebar with file upload and settings"""
        if not STREAMLIT_AVAILABLE:
            return
            
        st.sidebar.title("📚 PDF Chat Assistant")
        
        # Dependency status
        st.sidebar.subheader("🔧 System Status")
        deps = [
            ("Streamlit", STREAMLIT_AVAILABLE),
            ("LlamaIndex", LLAMA_INDEX_AVAILABLE),
            ("PyMuPDF Reader", PYMUPDF_READER_AVAILABLE),
            ("PyMuPDF", PYMUPDF_AVAILABLE),
        ]
        
        for name, available in deps:
            if available:
                st.sidebar.success(f"✅ {name}")
            else:
                st.sidebar.warning(f"⚠️ {name} (Mock mode)")
        
        # File upload
        st.sidebar.subheader("📄 Upload PDFs")
        uploaded_files = st.sidebar.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files to chat with"
        )
        
        # Parse method selection
        st.sidebar.subheader("⚙️ Parse Method")
        parse_method = st.sidebar.radio(
            "Select parsing method:",
            ["Quick Parse (PyMuPDF)", "Detailed Parse (LlamaParse)"],
            help="Quick Parse: Fast but basic text extraction\nDetailed Parse: Slower but better understanding of document structure"
        )
        
        # Process button
        if uploaded_files and st.sidebar.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                # Load environment variables
                self.load_environment_variables()
                
                # Process documents based on selected method
                if parse_method == "Quick Parse (PyMuPDF)":
                    documents = self.process_pdfs_quick_parse(uploaded_files)
                else:
                    documents = self.process_pdfs_llama_parse(uploaded_files)
                
                if documents:
                    # Create index
                    st.info("📊 Creating vector index...")
                    index = self.create_index(documents)
                    
                    if index:
                        # Create chat engine
                        st.info("🤖 Setting up chat engine...")
                        chat_engine = self.create_chat_engine(index)
                        
                        if chat_engine:
                            # Store in session state
                            st.session_state.index = index
                            st.session_state.chat_engine = chat_engine
                            st.session_state.documents_processed = True
                            st.success("✅ Documents processed successfully! You can now start chatting.")
                        else:
                            st.error("❌ Failed to create chat engine")
                    else:
                        st.error("❌ Failed to create index")
                else:
                    st.error("❌ No documents were processed successfully")
        
        # Clear button
        if st.sidebar.button("🗑️ Clear All"):
            st.session_state.documents_processed = False
            st.session_state.chat_history = []
            st.session_state.index = None
            st.session_state.chat_engine = None
            st.rerun()
        
        # Status
        st.sidebar.subheader("📊 Status")
        if st.session_state.documents_processed:
            st.sidebar.success("✅ Ready to chat!")
        else:
            st.sidebar.info("📤 Upload and process PDFs to start")
    
    def render_main_content(self):
        """Render the main chat interface"""
        if not STREAMLIT_AVAILABLE:
            self.print_demo_info()
            return
            
        st.title("💬 Chat with Your PDFs")
        
        if not st.session_state.documents_processed:
            st.info("👆 Please upload and process PDF documents using the sidebar to start chatting.")
            
            # Show example
            st.subheader("🎯 How to use:")
            st.markdown("""
            1. **Upload PDFs**: Use the sidebar to upload one or more PDF files
            2. **Choose Parse Method**: 
               - **Quick Parse**: Fast processing using PyMuPDF
               - **Detailed Parse**: Advanced processing using LlamaParse
            3. **Process**: Click the "Process Documents" button
            4. **Chat**: Ask questions about your documents in the chat interface
            """)
            
            # Show technical details
            st.subheader("🔧 Technical Features:")
            st.markdown("""
            - **Multi-PDF Support**: Upload and process multiple PDF files simultaneously
            - **Dual Parsing Methods**: 
              - PyMuPDFReader for fast, basic text extraction
              - LlamaParse for advanced document understanding with structure preservation
            - **Vector Indexing**: Uses LlamaIndex for efficient document retrieval
            - **Chat Memory**: Maintains conversation context for better responses
            - **Fallback Handling**: Graceful degradation when advanced features aren't available
            """)
            
            return
        
        # Chat interface
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chat_engine.chat(prompt)
                        response_text = str(response)
                        
                        # Display response
                        st.write(response_text)
                        
                        # Add to history
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": response_text
                        })
                        
                    except Exception as e:
                        error_msg = f"❌ Error generating response: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
    
    def print_demo_info(self):
        """Print demo information when Streamlit is not available"""
        print("\n" + "="*60)
        print("📚 PDF Chat Assistant - Demo Information")
        print("="*60)
        print("\n🎯 Application Features:")
        print("- Multi-PDF upload and processing")
        print("- Dual parsing methods (Quick/Detailed)")
        print("- Vector indexing for efficient retrieval")
        print("- Interactive chat interface")
        print("- Environment variable configuration")
        print("\n🔧 Technical Stack:")
        print("- Streamlit for the web interface")
        print("- LlamaIndex for document processing and retrieval")
        print("- PyMuPDF for fast PDF text extraction")
        print("- LlamaParse for advanced document understanding")
        print("- ChromaDB for vector storage (optional)")
        print("\n📦 To run the full application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: streamlit run pdf_chat_app.py")
        print("3. Access via browser: http://localhost:8501")
        print("\n" + "="*60 + "\n")
    
    def run(self):
        """Main application entry point"""
        if STREAMLIT_AVAILABLE:
            # Configure Streamlit page
            st.set_page_config(
                page_title="PDF Chat Assistant",
                page_icon="📚",
                layout="wide",
                initial_sidebar_state="expanded"
            )
            
            # Render sidebar
            self.render_sidebar()
            
            # Render main content
            self.render_main_content()
        else:
            # Demo mode
            self.print_demo_info()

def main():
    """Main function to run the Streamlit app"""
    app = PDFChatApp()
    app.run()

if __name__ == "__main__":
    main()