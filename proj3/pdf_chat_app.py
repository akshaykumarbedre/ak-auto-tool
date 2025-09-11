import streamlit as st
import os
import tempfile
from pathlib import Path
from typing import List, Any
import logging

# Import LlamaIndex components
from llama_index.core import VectorStoreIndex, StorageContext, ServiceContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine

# Import readers
from llama_index.readers.file import PyMuPDFReader
try:
    from llama_cloud import LlamaCloudReader
    LLAMA_PARSE_AVAILABLE = True
except ImportError:
    LLAMA_PARSE_AVAILABLE = False

# Import vector store
try:
    from llama_index.vector_stores.chroma import ChromaVectorStore
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Chat Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PDFChatApp:
    def __init__(self):
        self.index = None
        self.chat_engine = None
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
                        key, value = line.strip().split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"')
                        os.environ[key] = value
    
    def process_pdfs_quick_parse(self, uploaded_files: List[Any]) -> List[Any]:
        """Process PDFs using PyMuPDFReader (quick parse)"""
        documents = []
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
                    st.success(f"✅ Quick parse completed for {uploaded_file.name}")
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        return documents
    
    def process_pdfs_llama_parse(self, uploaded_files: List[Any]) -> List[Any]:
        """Process PDFs using LlamaParse (detailed parse)"""
        if not LLAMA_PARSE_AVAILABLE:
            st.error("❌ LlamaParse is not available. Please install llama-cloud.")
            return []
        
        documents = []
        
        try:
            reader = LlamaCloudReader(
                result_type="markdown",  # or "text"
                verbose=True
            )
            
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
                    st.success(f"✅ Detailed parse completed for {uploaded_file.name}")
                
        except Exception as e:
            st.error(f"❌ Error with LlamaParse: {str(e)}")
            st.info("💡 Falling back to quick parse...")
            return self.process_pdfs_quick_parse(uploaded_files)
        
        return documents
    
    def create_index(self, documents: List[Any]):
        """Create vector index from documents"""
        try:
            # Create node parser
            node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
            
            # Create storage context
            if CHROMA_AVAILABLE:
                # Use ChromaDB for vector storage
                chroma_client = chromadb.EphemeralClient()
                chroma_collection = chroma_client.create_collection("pdf_docs")
                vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
                storage_context = StorageContext.from_defaults(vector_store=vector_store)
            else:
                # Use default in-memory storage
                storage_context = StorageContext.from_defaults()
            
            # Create index
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
                node_parser=node_parser,
                show_progress=True
            )
            
            return index
            
        except Exception as e:
            st.error(f"❌ Error creating index: {str(e)}")
            return None
    
    def create_chat_engine(self, index):
        """Create chat engine from index"""
        try:
            # Create memory buffer
            memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
            
            # Create chat engine
            chat_engine = CondensePlusContextChatEngine.from_defaults(
                index,
                memory=memory,
                context_prompt=(
                    "You are a helpful assistant that answers questions based on the provided PDF documents. "
                    "Use the context from the documents to provide accurate and detailed responses. "
                    "If you cannot find relevant information in the documents, please say so."
                ),
                verbose=True
            )
            
            return chat_engine
            
        except Exception as e:
            st.error(f"❌ Error creating chat engine: {str(e)}")
            return None
    
    def render_sidebar(self):
        """Render the sidebar with file upload and settings"""
        st.sidebar.title("📚 PDF Chat Assistant")
        
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
    
    def run(self):
        """Main application entry point"""
        # Render sidebar
        self.render_sidebar()
        
        # Render main content
        self.render_main_content()

def main():
    """Main function to run the Streamlit app"""
    app = PDFChatApp()
    app.run()

if __name__ == "__main__":
    main()