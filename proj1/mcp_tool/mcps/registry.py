"""
MCP Registry Module
==================

Registry system for managing and accessing MCP functions.
Provides a centralized way to register, load, and query MCP retrievers.
"""

import os
import json
import logging
from typing import Dict, List, Any, Callable, Optional
from ..indexers.faiss_indexer import FAISSIndexer

logger = logging.getLogger(__name__)


class MCPRegistry:
    """
    Registry for managing MCP (Model Context Protocol) functions.
    """
    
    def __init__(self, registry_dir: str = "mcp_indices"):
        """
        Initialize the MCP registry.
        
        Args:
            registry_dir: Directory containing MCP index files
        """
        self.registry_dir = registry_dir
        self.registry_file = os.path.join(registry_dir, "registry.json")
        self._mcps: Dict[str, Callable] = {}
        self._indexers: Dict[str, FAISSIndexer] = {}
        self._load_registry()
    
    def _load_registry(self) -> None:
        """Load the registry from disk."""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r') as f:
                    registry_data = json.load(f)
                logger.info(f"Loaded registry with {len(registry_data)} MCPs")
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")
                registry_data = {}
        else:
            registry_data = {}
        
        self._registry_data = registry_data
    
    def _save_registry(self) -> None:
        """Save the registry to disk."""
        os.makedirs(self.registry_dir, exist_ok=True)
        try:
            with open(self.registry_file, 'w') as f:
                json.dump(self._registry_data, f, indent=2)
            logger.info(f"Saved registry with {len(self._registry_data)} MCPs")
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")
    
    def register_mcp(self, mcp_name: str, base_url: str, 
                    scrape_config: Dict[str, Any] = None) -> None:
        """
        Register a new MCP in the registry.
        
        Args:
            mcp_name: Name of the MCP
            base_url: Base URL that was scraped
            scrape_config: Configuration used for scraping
        """
        if scrape_config is None:
            scrape_config = {}
        
        self._registry_data[mcp_name] = {
            'base_url': base_url,
            'scrape_config': scrape_config,
            'created_at': self._get_timestamp()
        }
        
        self._save_registry()
        logger.info(f"Registered MCP '{mcp_name}' for URL: {base_url}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _load_indexer(self, mcp_name: str) -> FAISSIndexer:
        """Load an indexer for the given MCP."""
        if mcp_name not in self._indexers:
            try:
                indexer = FAISSIndexer()
                indexer.load_index(mcp_name, self.registry_dir)
                self._indexers[mcp_name] = indexer
                logger.info(f"Loaded indexer for MCP '{mcp_name}'")
            except Exception as e:
                logger.error(f"Failed to load indexer for MCP '{mcp_name}': {e}")
                raise
        
        return self._indexers[mcp_name]
    
    def _create_mcp_function(self, mcp_name: str) -> Callable:
        """Create a callable MCP function."""
        def mcp_query(query: str, k: int = 3) -> List[Dict[str, Any]]:
            """
            Query the MCP for relevant content.
            
            Args:
                query: Search query
                k: Number of results to return
                
            Returns:
                List of relevant documents with URL, text, and score
            """
            try:
                indexer = self._load_indexer(mcp_name)
                results = indexer.search(query, k)
                
                # Format results for MCP output
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        'url': result['url'],
                        'text': result['text'][:500] + '...' if len(result['text']) > 500 else result['text'],
                        'title': result.get('title', ''),
                        'score': result['score'],
                        'full_text': result['text']  # Include full text for advanced use
                    })
                
                return formatted_results
            
            except Exception as e:
                logger.error(f"Error querying MCP '{mcp_name}': {e}")
                return []
        
        return mcp_query
    
    def get_mcp(self, mcp_name: str) -> Optional[Callable]:
        """
        Get an MCP function by name.
        
        Args:
            mcp_name: Name of the MCP
            
        Returns:
            Callable MCP function or None if not found
        """
        if mcp_name not in self._registry_data:
            logger.warning(f"MCP '{mcp_name}' not found in registry")
            return None
        
        if mcp_name not in self._mcps:
            self._mcps[mcp_name] = self._create_mcp_function(mcp_name)
        
        return self._mcps[mcp_name]
    
    def __getitem__(self, mcp_name: str) -> Callable:
        """
        Get an MCP function using dictionary-like access.
        
        Args:
            mcp_name: Name of the MCP
            
        Returns:
            Callable MCP function
            
        Raises:
            KeyError: If MCP not found
        """
        mcp_func = self.get_mcp(mcp_name)
        if mcp_func is None:
            raise KeyError(f"MCP '{mcp_name}' not found")
        return mcp_func
    
    def list_mcps(self) -> List[str]:
        """
        List all registered MCP names.
        
        Returns:
            List of MCP names
        """
        return list(self._registry_data.keys())
    
    def get_mcp_info(self, mcp_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an MCP.
        
        Args:
            mcp_name: Name of the MCP
            
        Returns:
            Dictionary with MCP information
        """
        if mcp_name not in self._registry_data:
            return None
        
        info = self._registry_data[mcp_name].copy()
        
        # Add index statistics if available
        try:
            indexer = self._load_indexer(mcp_name)
            info['stats'] = indexer.get_stats()
        except Exception:
            info['stats'] = {'status': 'error'}
        
        return info
    
    def delete_mcp(self, mcp_name: str) -> bool:
        """
        Delete an MCP from the registry.
        
        Args:
            mcp_name: Name of the MCP to delete
            
        Returns:
            True if successfully deleted, False otherwise
        """
        if mcp_name not in self._registry_data:
            return False
        
        try:
            # Remove from registry
            del self._registry_data[mcp_name]
            
            # Remove from loaded MCPs
            if mcp_name in self._mcps:
                del self._mcps[mcp_name]
            
            # Remove from loaded indexers
            if mcp_name in self._indexers:
                del self._indexers[mcp_name]
            
            # Remove index files
            index_file = os.path.join(self.registry_dir, f"{mcp_name}_index.faiss")
            metadata_file = os.path.join(self.registry_dir, f"{mcp_name}_metadata.pkl")
            
            for file_path in [index_file, metadata_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            self._save_registry()
            logger.info(f"Deleted MCP '{mcp_name}'")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting MCP '{mcp_name}': {e}")
            return False


# Global registry instance
_registry = None


def get_registry() -> MCPRegistry:
    """
    Get the global MCP registry instance.
    
    Returns:
        MCPRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = MCPRegistry()
    return _registry


# Convenience access to the registry
MCP_REGISTRY = get_registry()