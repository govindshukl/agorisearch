#!/usr/bin/env python3
"""
Main entry point for the search engine project.
This script provides a command-line interface to run the search engine.
"""

import os
import sys
import asyncio
import argparse
from dotenv import load_dotenv

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.search_engine import create_search_graph
from src.core.search_engine_config import SearchConfig


async def run_search(query: str, config: SearchConfig = None):
    """
    Run a search with the given query.
    
    Args:
        query: The search query
        config: Optional search configuration
    
    Returns:
        The search results
    """
    if config is None:
        config = SearchConfig()
    
    # Create search graph
    search_graph = create_search_graph()
    
    # Create initial state
    initial_state = {
        "query": query
    }
    
    # Run the search graph
    print(f"Running search for query: {query}")
    result = await search_graph.ainvoke(
        initial_state,
        config=config.get_runnable_config()
    )
    
    return result


def main():
    """Main function to run the search engine from command line."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Search Engine CLI")
    parser.add_argument("query", nargs="?", type=str, help="Search query")
    parser.add_argument("--api", action="store_true", help="Run the API server")
    parser.add_argument("--port", type=int, default=8000, help="Port for API server")
    args = parser.parse_args()
    
    if args.api:
        # Run the API server
        import uvicorn
        from src.api.app import app
        print(f"Starting API server on port {args.port}...")
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    elif args.query:
        # Run a search query
        result = asyncio.run(run_search(args.query))
        
        # Print the result
        print("\n" + "="*80)
        print(f"Search Results for: {args.query}")
        print("="*80)
        print(result["response"])
        print("="*80)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
