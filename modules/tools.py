"""LangChain tools for document indexing and querying using PageIndex."""

import os
from typing import List, Union, Optional

from dotenv import load_dotenv
from langchain.tools import tool


from pageindex import PageIndexClient


from modules.vectorless import index_files, index_urls
from modules import get_logger

logger = get_logger(__name__)

load_dotenv()


@tool("index_files")
def index_files_tool(
    file_paths: Union[str, List[str]],
    api_key: Optional[str] = None,
) -> str:
    """Index local files (pdf, md, txt, csv, etc.) to PageIndex for searching.

    Args:
        file_paths: Single file path or list of file paths to index.
        api_key: Optional API key. Uses PAGE_INDEX_API_KEY env var if not provided.

    Returns:
        JSON string with indexed document info (doc_id, name, status, source).
    """
    key = api_key or os.getenv("PAGE_INDEX_API_KEY")
    if not key:
        logger.error("No API key provided")
        raise ValueError("API key required. Set PAGE_INDEX_API_KEY or pass api_key.")

    logger.info(f"Indexing files: {file_paths}")
    result = index_files(file_paths=file_paths, api_key=key)
    logger.info(f"Indexed {len(result)} files successfully")
    return str(result)


@tool("index_urls")
def index_urls_tool(
    urls: Union[str, List[str]],
    api_key: Optional[str] = None,
) -> str:
    """Index remote file URLs (pdf, md, txt, csv, etc.) to PageIndex for searching.

    Downloads the file, indexes it, and returns the document info.

    Args:
        urls: Single URL or list of URLs to index.
        api_key: Optional API key. Uses PAGE_INDEX_API_KEY env var if not provided.

    Returns:
        JSON string with indexed document info (doc_id, name, status, source).
    """
    key = api_key or os.getenv("PAGE_INDEX_API_KEY")
    if not key:
        logger.error("No API key provided")
        raise ValueError("API key required. Set PAGE_INDEX_API_KEY or pass api_key.")

    logger.info(f"Indexing URLs: {urls}")
    result = index_urls(urls=urls, api_key=key)
    logger.info(f"Indexed {len(result)} URLs successfully")
    return str(result)


@tool("query_index")
def query_index_tool(
    query: str,
    limit: int = 5,
    api_key: Optional[str] = None,
) -> str:
    """Query indexed documents from PageIndex to find relevant content.

    Args:
        query: Search query string.
        limit: Maximum number of results (default: 5).
        api_key: Optional API key. Uses PAGE_INDEX_API_KEY env var if not provided.

    Returns:
        JSON string with search results (content and metadata).
    """
    key = api_key or os.getenv("PAGE_INDEX_API_KEY")
    if not key:
        logger.error("No API key provided")
        raise ValueError("API key required. Set PAGE_INDEX_API_KEY or pass api_key.")

    if PageIndexClient is None:
        logger.error("PageIndexClient not installed")
        raise ImportError("pageindex package required. Install with: pip install pageindex")

    logger.info(f"Querying index: '{query}' (limit: {limit})")
    client = PageIndexClient(api_key=key)
    try:
        results = client.search(query=query, limit=limit)
        logger.info(f"Query returned {len(results) if results else 0} results")
        return str(results if results else [])
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise


def get_vectorless_tools():
    """Get all vectorless/index tools as a list."""
    logger.debug("get_vectorless_tools called")
    return [index_files_tool, index_urls_tool, query_index_tool]
