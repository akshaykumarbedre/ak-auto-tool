#!/usr/bin/env python3
"""
MCP Tool Demo - Standard Library Only
====================================

This demonstrates the MCP tool functionality using only Python standard library.
It simulates the document loading and search functionality.

Usage:
    python mcp_tool_demo.py --query "file operations"
"""

import argparse
import re
import sys
from typing import List, Dict, Any
from urllib.parse import urlparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockDocument:
    """Mock document class for demonstration."""
    
    def __init__(self, content: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.metadata = metadata or {}


class MockDocumentLoader:
    """Mock document loader with sample Python documentation content."""
    
    def __init__(self):
        # Sample documentation content (simulating loaded documents)
        self.sample_docs = [
            {
                'content': """
                File and Directory Access
                =========================
                
                The modules described in this chapter deal with disk files and directories. 
                For example, there are modules to read the properties of files, manipulate 
                paths in a portable way, and create temporary files. The full list of modules 
                in this chapter is:
                
                - pathlib — Object-oriented filesystem paths
                - os.path — Common pathname manipulations
                - fileinput — Iterate over lines from multiple input streams
                - stat — Interpreting stat() results
                - filecmp — File and directory comparisons
                - tempfile — Generate temporary files and directories
                - glob — Unix style pathname pattern expansion
                - fnmatch — Unix filename pattern matching
                - linecache — Random access to text lines
                - shutil — High-level file operations
                
                File I/O operations are fundamental to many Python programs. The os module 
                provides a portable way of using operating system dependent functionality.
                """,
                'metadata': {
                    'source': 'https://docs.python.org/3/library/filesys.html',
                    'title': 'File and Directory Access',
                    'section': 'Library Reference'
                }
            },
            {
                'content': """
                os.path — Common pathname manipulations
                ======================================
                
                This module implements some useful functions on pathnames. To read or write 
                files see open(), and for accessing the filesystem see the os module. The 
                path parameters can be passed as either strings, or bytes. Applications are 
                encouraged to represent file names as (Unicode) character strings.
                
                Functions:
                - os.path.abspath(path) - Return a normalized absolutized version of the pathname
                - os.path.basename(path) - Return the base name of pathname path
                - os.path.dirname(path) - Return the directory name of pathname path
                - os.path.exists(path) - Return True if path refers to an existing path
                - os.path.isfile(path) - Return True if path is an existing regular file
                - os.path.isdir(path) - Return True if path is an existing directory
                - os.path.join(path, *paths) - Join one or more path components intelligently
                - os.path.split(path) - Split the pathname path into a pair (head, tail)
                """,
                'metadata': {
                    'source': 'https://docs.python.org/3/library/os.path.html',
                    'title': 'os.path — Common pathname manipulations',
                    'section': 'Library Reference'
                }
            },
            {
                'content': """
                Built-in Functions
                ==================
                
                The Python interpreter has a number of functions and types built into it 
                that are always available. They are listed here in alphabetical order.
                
                open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, 
                     closefd=True, opener=None)
                
                Open file and return a corresponding file object. If the file cannot be 
                opened, an OSError is raised.
                
                file is a path-like object giving the pathname (absolute or relative to 
                the current working directory) of the file to be opened or an integer 
                file descriptor of the file to be wrapped.
                
                mode is an optional string that specifies the mode in which the file is 
                opened. It defaults to 'r' which means open for reading in text mode.
                
                Common modes:
                - 'r' - open for reading (default)
                - 'w' - open for writing, truncating the file first
                - 'x' - create a new file and open it for writing
                - 'a' - open for writing, appending to the end of the file if it exists
                - 'b' - binary mode
                - 't' - text mode (default)
                """,
                'metadata': {
                    'source': 'https://docs.python.org/3/library/functions.html#open',
                    'title': 'Built-in Functions - open()',
                    'section': 'Built-in Functions'
                }
            },
            {
                'content': """
                json — JSON encoder and decoder
                ==============================
                
                JSON (JavaScript Object Notation) is a lightweight data interchange format 
                inspired by JavaScript object literal syntax. This module can be used to 
                decode JSON data from strings or files.
                
                Basic usage:
                
                import json
                
                # Encode Python object to JSON string
                data = {'name': 'John', 'age': 30}
                json_string = json.dumps(data)
                
                # Decode JSON string to Python object
                python_object = json.loads(json_string)
                
                # Read from file
                with open('data.json', 'r') as f:
                    data = json.load(f)
                
                # Write to file
                with open('output.json', 'w') as f:
                    json.dump(data, f)
                
                Functions:
                - json.dumps() - Serialize obj to a JSON formatted string
                - json.loads() - Deserialize a JSON formatted string to a Python object
                - json.dump() - Serialize obj as a JSON formatted stream to fp
                - json.load() - Deserialize fp containing a JSON document to a Python object
                """,
                'metadata': {
                    'source': 'https://docs.python.org/3/library/json.html',
                    'title': 'json — JSON encoder and decoder',
                    'section': 'Library Reference'
                }
            },
            {
                'content': """
                Error Handling and Exceptions
                ============================
                
                Even if a statement or expression is syntactically correct, it may cause 
                an error when an attempt is made to execute it. Errors detected during 
                execution are called exceptions and are not unconditionally fatal.
                
                Built-in Exceptions:
                
                exception OSError - This exception is raised when a system function returns 
                a system-related error, including I/O failures such as "file not found" or 
                "disk full".
                
                exception FileNotFoundError - A subclass of OSError, raised when a file or 
                directory is requested but doesn't exist.
                
                exception PermissionError - A subclass of OSError, raised when trying to 
                run an operation without the adequate access rights.
                
                Try-except blocks:
                
                try:
                    with open('file.txt', 'r') as f:
                        content = f.read()
                except FileNotFoundError:
                    print("File not found")
                except PermissionError:
                    print("Permission denied")
                except OSError as e:
                    print(f"OS error: {e}")
                """,
                'metadata': {
                    'source': 'https://docs.python.org/3/tutorial/errors.html',
                    'title': 'Error Handling and Exceptions',
                    'section': 'Tutorial'
                }
            }
        ]
    
    def load_documentation(self, base_url: str) -> List[MockDocument]:
        """Load sample documentation (simulates web scraping)."""
        logger.info(f"Loading documentation from: {base_url}")
        
        documents = []
        for doc_data in self.sample_docs:
            doc = MockDocument(
                content=doc_data['content'],
                metadata=doc_data['metadata']
            )
            documents.append(doc)
        
        logger.info(f"Successfully loaded {len(documents)} documents")
        return documents


class SimpleSearchEngine:
    """Simple search engine using keyword matching."""
    
    def __init__(self, documents: List[MockDocument]):
        self.documents = documents
        self._build_index()
    
    def _build_index(self):
        """Build a simple keyword index."""
        self.word_index = {}
        
        for i, doc in enumerate(self.documents):
            # Extract words from content
            words = re.findall(r'\b\w+\b', doc.content.lower())
            for word in set(words):
                if len(word) > 2:  # Skip very short words
                    if word not in self.word_index:
                        self.word_index[word] = []
                    self.word_index[word].append(i)
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for documents matching the query."""
        query_words = re.findall(r'\b\w+\b', query.lower())
        query_words = [w for w in query_words if len(w) > 2]
        
        if not query_words:
            return []
        
        # Calculate scores for each document
        doc_scores = {}
        
        for word in query_words:
            if word in self.word_index:
                for doc_idx in self.word_index[word]:
                    if doc_idx not in doc_scores:
                        doc_scores[doc_idx] = 0
                    doc_scores[doc_idx] += 1
        
        # Sort by score and return top k
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        
        for i, (doc_idx, score) in enumerate(sorted_docs[:k]):
            doc = self.documents[doc_idx]
            
            # Find relevant excerpts
            content_lower = doc.content.lower()
            excerpts = []
            for word in query_words:
                if word in content_lower:
                    # Find sentences containing the word
                    sentences = re.split(r'[.!?]\s+', doc.content)
                    for sentence in sentences:
                        if word in sentence.lower():
                            excerpts.append(sentence.strip())
                            break
            
            # Create excerpt or use beginning of content
            excerpt = ' '.join(excerpts[:2]) if excerpts else doc.content[:300]
            
            result = {
                'rank': i + 1,
                'content': doc.content,
                'excerpt': excerpt,
                'metadata': doc.metadata,
                'source': doc.metadata.get('source', 'Unknown'),
                'title': doc.metadata.get('title', 'Untitled'),
                'relevance_score': score / len(query_words)
            }
            results.append(result)
        
        return results


class MCPToolDemo:
    """MCP Tool demonstration class."""
    
    def __init__(self):
        self.loader = MockDocumentLoader()
        self.documents = []
        self.search_engine = None
    
    def load_documentation(self, base_url: str) -> List[MockDocument]:
        """Load documentation from URL (simulated)."""
        self.documents = self.loader.load_documentation(base_url)
        self.search_engine = SimpleSearchEngine(self.documents)
        return self.documents
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search the loaded documents."""
        if not self.search_engine:
            raise ValueError("No documents loaded. Please load documentation first.")
        
        return self.search_engine.search(query, k)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get document statistics."""
        if not self.documents:
            return {"total_documents": 0}
        
        total_chars = sum(len(doc.content) for doc in self.documents)
        sources = set(doc.metadata.get('source', 'Unknown') for doc in self.documents)
        
        return {
            'total_documents': len(self.documents),
            'total_characters': total_chars,
            'average_document_length': total_chars / len(self.documents),
            'unique_sources': len(sources),
            'sources': list(sources)
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="MCP Tool Demo - Standard Library Only")
    parser.add_argument("--url", default="https://docs.python.org/3/", 
                       help="Base URL to load documentation from (simulated)")
    parser.add_argument("--query", default="file operations", 
                       help="Search query (default: 'file operations')")
    parser.add_argument("--results", type=int, default=3, 
                       help="Number of results to return")
    parser.add_argument("--stats", action="store_true", 
                       help="Show document statistics")
    
    args = parser.parse_args()
    
    try:
        print("🚀 MCP Tool Demo - Document Loading and Retrieval")
        print("=" * 60)
        
        # Create the tool
        tool = MCPToolDemo()
        
        # Load documentation
        print(f"📚 Loading documentation from: {args.url}")
        documents = tool.load_documentation(args.url)
        
        # Show statistics
        stats = tool.get_stats()
        print(f"✅ Loaded {stats['total_documents']} documents")
        
        if args.stats:
            print("\n📊 Document Statistics:")
            print(f"   Total documents: {stats['total_documents']}")
            print(f"   Total characters: {stats['total_characters']:,}")
            print(f"   Average document length: {stats['average_document_length']:.0f} characters")
            print(f"   Unique sources: {stats['unique_sources']}")
            print("\n   Sources:")
            for source in stats['sources']:
                print(f"   - {source}")
        
        # Perform search
        print(f"\n🔍 Searching for: '{args.query}'")
        results = tool.search(args.query, k=args.results)
        
        if results:
            print(f"\n🎯 Search Results ({len(results)} found):")
            print("=" * 60)
            
            for result in results:
                print(f"\n📄 Rank {result['rank']}: {result['title']}")
                print(f"🔗 Source: {result['source']}")
                print(f"⭐ Relevance Score: {result['relevance_score']:.2f}")
                print("📝 Excerpt:")
                print(f"   {result['excerpt'][:400]}...")
                print("-" * 40)
        else:
            print("❌ No results found.")
        
        # Demonstrate different queries
        print("\n🔄 Trying different search queries:")
        test_queries = ["json parsing", "error handling", "open file"]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            results = tool.search(query, k=2)
            if results:
                for result in results[:1]:  # Show only first result
                    print(f"   📄 {result['title']} (Score: {result['relevance_score']:.2f})")
            else:
                print("   ❌ No results found")
        
        print("\n✅ MCP Tool Demo completed successfully!")
        print("\n💡 This demo shows how the MCP tool would work with real documentation.")
        print("📚 In the full version, it would load actual documentation from URLs")
        print("🔍 and provide advanced search capabilities with vector embeddings.")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()