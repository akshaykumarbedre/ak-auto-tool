#!/usr/bin/env python3
"""
MCP Tool for Document Loading and Retrieval
===========================================

This tool provides an MCP (Model Context Protocol) interface for loading documentation
from URLs and enabling hybrid search capabilities.

Usage:
    python mcp_tool.py --url "https://docs.python.org/3.9/" --query "file operations"
    python mcp_tool.py --url "https://langchain.readthedocs.io/" --query "document loaders"
"""

import argparse
import logging
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleVectorStore:
    """Simple vector store using sklearn TF-IDF and cosine similarity."""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.doc_vectors = None
        self._build_index()
    
    def _build_index(self):
        """Build the TF-IDF index from documents."""
        texts = [doc.page_content for doc in self.documents]
        self.doc_vectors = self.vectorizer.fit_transform(texts)
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search."""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include documents with some similarity
                doc = self.documents[idx]
                # Add similarity score as metadata
                doc.metadata['similarity_score'] = similarities[idx]
                results.append(doc)
        
        return results


class DocumentLoaderTool:
    """
    A tool for loading documentation from URLs and providing hybrid search capabilities.
    """
    
    def __init__(self, max_depth: int = 2, timeout: int = 10):
        """
        Initialize the document loader tool.
        
        Args:
            max_depth: Maximum depth for recursive URL loading
            timeout: Timeout for URL requests
        """
        self.max_depth = max_depth
        self.timeout = timeout
        self.documents: List[Document] = []
        self.vectorstore = None
        
    def load_documentation(self, base_url: str, **kwargs) -> List[Document]:
        """
        Load documentation from a base URL using RecursiveUrlLoader.
        
        Args:
            base_url: The base URL to start loading from
            **kwargs: Additional parameters for RecursiveUrlLoader
            
        Returns:
            List of loaded documents
        """
        logger.info(f"Loading documentation from: {base_url}")
        
        # Set up default parameters
        loader_params = {
            "max_depth": self.max_depth,
            "timeout": self.timeout,
            "check_response_status": True,
            "continue_on_failure": True,
            "prevent_outside": True,
            **kwargs
        }
        
        try:
            # Create the loader
            loader = RecursiveUrlLoader(base_url, **loader_params)
            
            # Load documents
            self.documents = loader.load()
            logger.info(f"Successfully loaded {len(self.documents)} documents")
            
            return self.documents
            
        except Exception as e:
            logger.error(f"Error loading documentation: {str(e)}")
            raise
    
    def create_retriever(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Create a retriever from the loaded documents.
        
        Args:
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        if not self.documents:
            raise ValueError("No documents loaded. Please load documentation first.")
        
        logger.info("Creating retriever from loaded documents...")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        
        texts = text_splitter.split_documents(self.documents)
        logger.info(f"Split documents into {len(texts)} chunks")
        
        # Create vector store
        self.vectorstore = SimpleVectorStore(texts)
        logger.info("Vector store created successfully")
        
        return self.vectorstore
    
    def hybrid_search(self, query: str, k: int = 5, search_type: str = "similarity") -> List[Dict[str, Any]]:
        """
        Perform hybrid search on the loaded documents.
        
        Args:
            query: Search query
            k: Number of results to return
            search_type: Type of search (currently only "similarity" supported)
            
        Returns:
            List of search results with metadata
        """
        if not self.vectorstore:
            raise ValueError("Retriever not created. Please create retriever first.")
        
        logger.info(f"Performing hybrid search for query: '{query}'")
        
        # Perform search
        results = self.vectorstore.similarity_search(query, k=k)
        
        # Format results
        formatted_results = []
        for i, doc in enumerate(results):
            result = {
                "rank": i + 1,
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": doc.metadata.get("source", "Unknown"),
                "relevance_score": doc.metadata.get("similarity_score", 0.0)
            }
            formatted_results.append(result)
        
        logger.info(f"Found {len(formatted_results)} relevant documents")
        return formatted_results
    
    def get_document_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the loaded documents.
        
        Returns:
            Dictionary with document statistics
        """
        if not self.documents:
            return {"total_documents": 0}
        
        total_chars = sum(len(doc.page_content) for doc in self.documents)
        sources = set(doc.metadata.get("source", "Unknown") for doc in self.documents)
        
        return {
            "total_documents": len(self.documents),
            "total_characters": total_chars,
            "average_document_length": total_chars / len(self.documents),
            "unique_sources": len(sources),
            "sources": list(sources)
        }


def main():
    """
    Main function to run the MCP tool from command line.
    """
    parser = argparse.ArgumentParser(description="MCP Tool for Document Loading and Retrieval")
    parser.add_argument("--url", required=True, help="Base URL to load documentation from")
    parser.add_argument("--query", help="Search query for hybrid search")
    parser.add_argument("--max-depth", type=int, default=2, help="Maximum depth for recursive loading")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for URL requests")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size for text splitting")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap for text splitting")
    parser.add_argument("--results", type=int, default=5, help="Number of search results to return")
    parser.add_argument("--search-type", default="similarity", choices=["similarity"], 
                       help="Type of search to perform")
    parser.add_argument("--stats", action="store_true", help="Show document statistics")
    
    args = parser.parse_args()
    
    try:
        # Create the tool
        tool = DocumentLoaderTool(max_depth=args.max_depth, timeout=args.timeout)
        
        # Load documentation
        print(f"Loading documentation from: {args.url}")
        documents = tool.load_documentation(args.url)
        
        # Show statistics if requested
        if args.stats:
            stats = tool.get_document_stats()
            print("\nDocument Statistics:")
            print(f"Total documents: {stats['total_documents']}")
            print(f"Total characters: {stats['total_characters']:,}")
            print(f"Average document length: {stats['average_document_length']:.0f} characters")
            print(f"Unique sources: {stats['unique_sources']}")
        
        # Create retriever
        print("Creating retriever...")
        retriever = tool.create_retriever(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
        
        # Perform search if query provided
        if args.query:
            print(f"\nPerforming hybrid search for: '{args.query}'")
            results = tool.hybrid_search(args.query, k=args.results, search_type=args.search_type)
            
            print(f"\nSearch Results ({len(results)} found):")
            print("=" * 80)
            
            for result in results:
                print(f"\nRank {result['rank']}: {result['source']}")
                print("-" * 40)
                print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
                print(f"Relevance Score: {result['relevance_score']:.3f}")
                print()
        
        print("\nMCP Tool execution completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()