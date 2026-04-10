"""Module for indexing documents using PageIndex client."""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Dict, Any

import requests
from pageindex import PageIndexClient

from modules import get_logger

logger = get_logger(__name__)


def index_documents(
    sources: Union[str, List[str]],
    api_key: str,
    max_workers: int = 10,
    poll_interval: int = 5,
    timeout: int = 300,
) -> List[Dict[str, Any]]:
    """
    Index documents (files or URLs) using PageIndex service.

    Args:
        sources: A single file path/URL (str) or list of file paths/URLs (list).
                Supported types: md, pdf, txt, csv, and other common formats.
        api_key: PageIndex API key.
        max_workers: Maximum number of parallel workers (default: 10).
        poll_interval: Seconds between status checks (default: 5).
        timeout: Maximum seconds to wait for completion (default: 300).

    Returns:
        List of dictionaries containing indexed document information.
                Each dict contains: 'doc_id', 'name', 'status', 'source'.

    Raises:
        ValueError: If api_key is not provided or sources is empty.
        ImportError: If pageindex package is not installed.
    """
    if not api_key:
        raise ValueError("API key is required")

    if not sources:
        raise ValueError("Sources cannot be empty")

    if isinstance(sources, str):
        sources = [sources]

    if PageIndexClient is None:
        raise ImportError("pageindex package is required. Install with: pip install pageindex")

    results: List[Dict[str, Any]] = []

    def _process_single_source(source: str) -> Dict[str, Any]:
        """Process a single source (download if URL, then index)."""
        try:
            local_path = source

            if source.startswith(("http://", "https://")):
                filename = source.split("/")[-1]
                local_path = os.path.join("../data", filename)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                if not os.path.exists(local_path):
                    response = requests.get(source, timeout=60)
                    response.raise_for_status()
                    with open(local_path, "wb") as f:
                        f.write(response.content)

            if not os.path.exists(local_path):
                return {
                    "source": source,
                    "status": "error",
                    "error": f"File not found: {local_path}",
                }

            pi = PageIndexClient(api_key=api_key)
            submit_result = pi.submit_document(local_path)
            doc_id = submit_result.get("doc_id")

            start_time = time.time()
            while time.time() - start_time < timeout:
                status_result = pi.get_document(doc_id)
                status = status_result.get("status")

                if status == "completed":
                    return {
                        "doc_id": doc_id,
                        "name": status_result.get("name"),
                        "status": "completed",
                        "source": source,
                    }
                elif status in ("failed", "error"):
                    return {
                        "doc_id": doc_id,
                        "status": "failed",
                        "source": source,
                        "error": status_result.get("error", "Unknown error"),
                    }

                time.sleep(poll_interval)

            return {
                "doc_id": doc_id,
                "status": "timeout",
                "source": source,
            }

        except requests.RequestException as e:
            return {"source": source, "status": "error", "error": str(e)}
        except Exception as e:
            logger.error(f"Error indexing {source}: {e}")
            return {"source": source, "status": "error", "error": str(e)}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_single_source, src): src for src in sources}

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            logger.info(f"Indexed: {result.get('source')} - Status: {result.get('status')}")

    return results


def index_files(
    file_paths: Union[str, List[str]],
    api_key: str,
    **kwargs,
) -> List[Dict[str, Any]]:
    """
    Index local files using PageIndex service.

    Alias for index_documents with file path focus.

    Args:
        file_paths: A single file path or list of file paths.
        api_key: PageIndex API key.
        **kwargs: Additional arguments passed to index_documents.

    Returns:
        List of dictionaries containing indexed document information.
    """
    return index_documents(sources=file_paths, api_key=api_key, **kwargs)


def index_urls(
    urls: Union[str, List[str]],
    api_key: str,
    **kwargs,
) -> List[Dict[str, Any]]:
    """
    Index remote URLs (files) using PageIndex service.

    Alias for index_documents with URL focus.

    Args:
        urls: A single URL or list of URLs.
        api_key: PageIndex API key.
        **kwargs: Additional arguments passed to index_documents.

    Returns:
        List of dictionaries containing indexed document information.
    """
    return index_documents(sources=urls, api_key=api_key, **kwargs)
