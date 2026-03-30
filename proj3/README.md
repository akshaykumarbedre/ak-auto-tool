# 📚 PDF Chat Assistant

A powerful Streamlit application that allows users to upload multiple PDF documents, process them using advanced parsing methods, and interact with the content through an intelligent chat interface.

## 🎯 Features

### Core Functionality
- **Multi-PDF Upload**: Upload and process multiple PDF files simultaneously
- **Dual Parsing Methods**: 
  - **Quick Parse**: Fast text extraction using PyMuPDFReader
  - **Detailed Parse**: Advanced document understanding using LlamaParse with structure preservation
- **Vector Indexing**: Efficient document retrieval using LlamaIndex
- **Interactive Chat**: Ask questions about your documents with conversational memory
- **Real-time Processing**: Live status updates during document processing

### Technical Features
- **Fallback Handling**: Graceful degradation when advanced features aren't available
- **Environment Configuration**: Secure API key management via `.env` files
- **Session Management**: Persistent chat history and document state
- **Error Handling**: Comprehensive error reporting and recovery
- **Modular Design**: Clean separation of concerns for easy maintenance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- LLAMA_CLOUD_API_KEY (for detailed parsing)

### Installation

1. **Clone and navigate to the project:**
```bash
cd proj3
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create or update `notebook/.env` with your API key:
```
LLAMA_CLOUD_API_KEY="your-api-key-here"
```

4. **Run the application:**
```bash
streamlit run pdf_chat_app.py
```

5. **Access the app:**
Open your browser and go to `http://localhost:8501`

### Demo Mode
If dependencies are not installed, you can run the demo version:
```bash
python3 pdf_chat_demo.py
```

## 📖 Usage Guide

### Step 1: Upload Documents
- Use the sidebar to upload one or more PDF files
- Supported format: PDF files only
- Multiple files can be processed simultaneously

### Step 2: Choose Processing Method
- **Quick Parse (PyMuPDF)**: 
  - Fast processing
  - Basic text extraction
  - Good for simple documents
  
- **Detailed Parse (LlamaParse)**:
  - Advanced processing with AI
  - Preserves document structure
  - Better for complex layouts, tables, and figures
  - Requires LLAMA_CLOUD_API_KEY

### Step 3: Process Documents
- Click "🚀 Process Documents" button
- Wait for processing to complete
- Status updates will show progress

### Step 4: Start Chatting
- Use the chat input at the bottom
- Ask questions about your documents
- The AI will search through your documents to provide relevant answers
- Chat history is maintained throughout the session

### Step 5: Manage Session
- Use "🗑️ Clear All" to reset everything
- Upload new documents anytime
- Switch between parsing methods as needed

## 🔧 Technical Architecture

### Components

1. **PDFChatApp Class**: Main application controller
2. **Document Processing**: 
   - PyMuPDFReader for quick parsing
   - LlamaCloudReader for detailed parsing
3. **Indexing System**: 
   - VectorStoreIndex for document retrieval
   - SentenceSplitter for text chunking
   - Optional ChromaDB integration
4. **Chat Engine**: 
   - CondensePlusContextChatEngine for conversations
   - ChatMemoryBuffer for context retention
5. **UI Components**: 
   - Streamlit sidebar for controls
   - Main chat interface
   - Status and progress indicators

### File Structure
```
proj3/
├── pdf_chat_app.py          # Main application
├── pdf_chat_demo.py         # Demo version
├── requirements.txt         # Dependencies
├── run_app.sh              # Run script
├── test_imports.sh         # Dependency checker
├── notebook/
│   ├── .env                # Environment variables
│   └── ...                 # Other notebook files
└── README.md               # This file
```

## 🛠️ Configuration

### Environment Variables
- `LLAMA_CLOUD_API_KEY`: Required for LlamaParse functionality

### Optional Dependencies
- `chromadb`: For advanced vector storage
- `llama-cloud`: For detailed document parsing

### Streamlit Configuration
The app automatically configures Streamlit with:
- Wide layout for better chat experience
- Expanded sidebar for easy access to controls
- Custom page title and icon

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: 
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

2. **LlamaParse Not Working**:
   - Verify LLAMA_CLOUD_API_KEY in `.env` file
   - Check internet connectivity
   - Falls back to quick parse automatically

3. **Memory Issues**:
   - Reduce chunk size in node parser
   - Process fewer documents simultaneously
   - Clear session state regularly

4. **Streamlit Not Found**:
   - Install streamlit: `pip install streamlit`
   - Use demo version: `python3 pdf_chat_demo.py`

### Debug Mode
Enable verbose logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security Notes

- API keys are loaded from `.env` files (not committed to git)
- Temporary files are automatically cleaned up
- No persistent storage of uploaded documents
- Session data is cleared on browser refresh

## 🚧 Future Enhancements

- [ ] Support for additional file formats (DOCX, TXT)
- [ ] Advanced search and filtering capabilities
- [ ] Document comparison features
- [ ] Export chat history
- [ ] Multi-language support
- [ ] Custom embedding models
- [ ] Batch processing capabilities

## 📝 License

This project is part of the ak-auto-tool repository and follows the same licensing terms.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

---

**Note**: This application requires active internet connectivity for LlamaParse functionality and AI-powered responses. The quick parse mode works offline for basic text extraction.