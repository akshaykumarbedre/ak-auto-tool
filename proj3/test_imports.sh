#!/bin/bash

# Test script for PDF Chat App
echo "🚀 Testing PDF Chat App Dependencies..."

cd /home/runner/work/ak-auto-tool/ak-auto-tool/proj3

# Check if we can import the required modules
python3 -c "
import sys
try:
    import streamlit
    print('✅ Streamlit: Available')
except ImportError:
    print('❌ Streamlit: Missing')
    sys.exit(1)

try:
    from llama_index.core import VectorStoreIndex
    print('✅ LlamaIndex Core: Available')
except ImportError:
    print('❌ LlamaIndex Core: Missing')

try:
    from llama_index.readers.file import PyMuPDFReader
    print('✅ PyMuPDFReader: Available')
except ImportError:
    print('❌ PyMuPDFReader: Missing')

try:
    import pymupdf
    print('✅ PyMuPDF: Available')
except ImportError:
    print('❌ PyMuPDF: Missing')

try:
    from llama_cloud import LlamaCloudReader
    print('✅ LlamaCloud: Available')
except ImportError:
    print('⚠️  LlamaCloud: Missing (optional)')

try:
    import chromadb
    print('✅ ChromaDB: Available')
except ImportError:
    print('⚠️  ChromaDB: Missing (optional)')

print('🔧 Basic import test completed!')
"