"""
FAISS Indexer Module
==================

Handles embedding generation using SentenceTransformers and FAISS storage.
Provides efficient semantic search capabilities for scraped website content.
"""

import pickle
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = logging.getLogger(__name__)


class FAISSIndexer:
    """
    FAISS-based indexer for semantic search using SentenceTransformer embeddings.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the FAISS indexer.
        
        Args:
            model_name: Name of the SentenceTransformer model to use
        """
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required. Install with: pip install sentence-transformers")
        
        if faiss is None:
            raise ImportError("faiss is required. Install with: pip install faiss-cpu")
        
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.dimension = None
        
    def build_index(self, documents: List[Dict[str, str]], mcp_name: str, 
                   save_dir: str = "mcp_indices") -> None:
        """
        Build FAISS index from documents and save to disk.
        
        Args:
            documents: List of document dictionaries with 'url' and 'text' keys
            mcp_name: Name for the MCP (used for file naming)
            save_dir: Directory to save index files
        """
        if not documents:
            raise ValueError("No documents provided for indexing")
        
        logger.info(f"Building FAISS index for {len(documents)} documents")
        
        # Extract text content
        texts = [doc['text'] for doc in documents]
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        self.dimension = embeddings.shape[1]
        logger.info(f"Creating FAISS index with dimension {self.dimension}")
        
        # Use IndexFlatIP for cosine similarity (after normalization)
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents for retrieval
        self.documents = documents
        
        # Save to disk
        os.makedirs(save_dir, exist_ok=True)
        
        index_path = os.path.join(save_dir, f"{mcp_name}_index.faiss")
        metadata_path = os.path.join(save_dir, f"{mcp_name}_metadata.pkl")
        
        # Save FAISS index
        faiss.write_index(self.index, index_path)
        
        # Save metadata
        metadata = {
            'documents': documents,
            'model_name': self.model_name,
            'dimension': self.dimension,
            'mcp_name': mcp_name
        }
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        logger.info(f"Index saved to {index_path}")
        logger.info(f"Metadata saved to {metadata_path}")
    
    def load_index(self, mcp_name: str, save_dir: str = "mcp_indices") -> None:
        """
        Load FAISS index from disk.
        
        Args:
            mcp_name: Name of the MCP to load
            save_dir: Directory containing index files
        """
        index_path = os.path.join(save_dir, f"{mcp_name}_index.faiss")
        metadata_path = os.path.join(save_dir, f"{mcp_name}_metadata.pkl")
        
        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Index files not found for MCP '{mcp_name}' in {save_dir}")
        
        # Load FAISS index
        self.index = faiss.read_index(index_path)
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        self.documents = metadata['documents']
        self.model_name = metadata['model_name']
        self.dimension = metadata['dimension']
        
        # Ensure model is loaded
        if self.model is None or self.model.get_sentence_embedding_dimension() != self.dimension:
            logger.info(f"Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        
        logger.info(f"Loaded index for MCP '{mcp_name}' with {len(self.documents)} documents")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar documents using the query.
        
        Args:
            query: Search query
            k: Number of top results to return
            
        Returns:
            List of dictionaries with 'url', 'text', 'score', and 'title' keys
        """
        if self.index is None:
            raise ValueError("Index not loaded. Call build_index() or load_index() first.")
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Format results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx >= 0:  # Valid index
                doc = self.documents[idx]
                results.append({
                    'url': doc['url'],
                    'text': doc['text'],
                    'title': doc.get('title', ''),
                    'score': float(score),
                    'rank': i + 1
                })
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index.
        
        Returns:
            Dictionary with index statistics
        """
        if self.index is None:
            return {'status': 'not_loaded'}
        
        return {
            'status': 'loaded',
            'total_documents': len(self.documents),
            'dimension': self.dimension,
            'model_name': self.model_name,
            'index_size': self.index.ntotal
        }


def build_index(documents: List[Dict[str, str]], mcp_name: str, 
               model_name: str = "all-MiniLM-L6-v2", 
               save_dir: str = "mcp_indices") -> None:
    """
    Convenience function to build a FAISS index.
    
    Args:
        documents: List of document dictionaries
        mcp_name: Name for the MCP
        model_name: SentenceTransformer model name
        save_dir: Directory to save index files
    """
    indexer = FAISSIndexer(model_name)
    indexer.build_index(documents, mcp_name, save_dir)


def load_index(mcp_name: str, save_dir: str = "mcp_indices") -> FAISSIndexer:
    """
    Convenience function to load a FAISS index.
    
    Args:
        mcp_name: Name of the MCP to load
        save_dir: Directory containing index files
        
    Returns:
        Loaded FAISSIndexer instance
    """
    indexer = FAISSIndexer()
    indexer.load_index(mcp_name, save_dir)
    return indexer