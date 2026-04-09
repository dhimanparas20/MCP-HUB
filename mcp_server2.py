from fastmcp import FastMCP
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Any

mcp = FastMCP("filesystem")
ROOT = os.getenv("FILESYSTEM_ROOT", "D:\\0Coding")
if ROOT.endswith("\\"):
    ROOT = ROOT[:-1]


def _format_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def safe(path: str) -> str:
    full = os.path.normpath(os.path.join(ROOT, path))
    if not full.startswith(ROOT):
        raise ValueError("Access denied: outside allowed directory")
    return full


@mcp.tool(
    name="list_directory",
    description="List contents of a directory with optional filtering.",
    tags={"enabled"},
)
def list_directory(path: str = ".", pattern: str | None = None, include_hidden: bool = False) -> dict[str, Any]:
    """List contents of a directory.

    Args:
        path: Path to the directory.
        pattern: Optional glob pattern to filter files.
        include_hidden: Whether to include hidden files (starting with .).

    Returns:
        dict: Directory listing with files and subdirectories.
    """
    full = safe(path)
    if not os.path.exists(full):
        return {"ok": False, "error": f"Directory not found: {path}"}
    if not os.path.isdir(full):
        return {"ok": False, "error": f"Not a directory: {path}"}

    items = []
    for item in os.listdir(full):
        if not include_hidden and item.startswith("."):
            continue
        full_path = os.path.join(full, item)
        stat = os.stat(full_path)
        if pattern and not Path(item).match(pattern):
            continue
        items.append(
            {
                "name": item,
                "path": os.path.join(path, item),
                "is_file": os.path.isfile(full_path),
                "is_dir": os.path.isdir(full_path),
                "size_bytes": stat.st_size if os.path.isfile(full_path) else None,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
        )

    items.sort(key=lambda x: (not x["is_dir"], x["name"]))
    return {"ok": True, "path": path, "items": items, "count": len(items)}


@mcp.tool(
    name="get_file_info",
    description="Get detailed information about a file.",
    tags={"enabled"},
)
def get_file_info(path: str) -> dict[str, Any]:
    """Get detailed information about a file.

    Args:
        path: Path to the file.

    Returns:
        dict: File details including size, modified time, etc.
    """
    full = safe(path)
    if not os.path.exists(full):
        return {"ok": False, "error": f"File not found: {path}"}

    stat = os.stat(full)
    p = Path(full)
    return {
        "ok": True,
        "name": p.name,
        "path": path,
        "size_bytes": stat.st_size,
        "size_readable": _format_size(stat.st_size),
        "is_file": p.is_file(),
        "is_dir": p.is_dir(),
        "is_symlink": p.is_symlink(),
        "exists": p.exists(),
        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "extension": p.suffix,
        "parent": str(p.parent),
    }


@mcp.tool(
    name="read_file",
    description="Read content from a file.",
    tags={"enabled"},
)
def read_file(path: str, max_size: int = 1024 * 1024) -> dict[str, Any]:
    """Read content from a file.

    Args:
        path: Path to the file.
        max_size: Maximum file size to read in bytes (default 1MB).

    Returns:
        dict: File content and metadata.
    """
    full = safe(path)
    if not os.path.exists(full):
        return {"ok": False, "error": f"File not found: {path}"}
    if not os.path.isfile(full):
        return {"ok": False, "error": f"Not a file: {path}"}

    size = os.path.getsize(full)
    if size > max_size:
        return {"ok": False, "error": f"File too large: {size} bytes (max {max_size})"}

    with open(full, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "ok": True,
        "path": path,
        "content": content,
        "size_bytes": size,
        "lines": len(content.splitlines()),
    }


@mcp.tool(
    name="write_file",
    description="Write content to a file, creating or overwriting.",
    tags={"enabled"},
)
def write_file(path: str, content: str, create_dirs: bool = True) -> dict[str, Any]:
    """Write content to a file.

    Args:
        path: Path to the file.
        content: Content to write.
        create_dirs: Whether to create parent directories.

    Returns:
        dict: Operation status.
    """
    full = safe(path)

    if create_dirs:
        os.makedirs(os.path.dirname(full), exist_ok=True)

    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "ok": True,
        "path": path,
        "size_bytes": len(content.encode("utf-8")),
    }


@mcp.tool(
    name="create_file",
    description="Create a new file with optional content.",
    tags={"enabled"},
)
def create_file(path: str, content: str = "", create_dirs: bool = True) -> dict[str, Any]:
    """Create a new file with optional content.

    Args:
        path: Path for the new file.
        content: Content to write to the file.
        create_dirs: Whether to create parent directories if they don't exist.

    Returns:
        dict: Operation status with created file path.
    """
    full = safe(path)

    if create_dirs:
        os.makedirs(os.path.dirname(full), exist_ok=True)
    else:
        if not os.path.exists(os.path.dirname(full)):
            return {
                "ok": False,
                "error": f"Parent directory does not exist: {os.path.dirname(path)}",
            }

    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

    return {"ok": True, "path": path, "size_bytes": len(content.encode("utf-8"))}


@mcp.tool(
    name="copy_file",
    description="Copy a file or directory to a new location.",
    tags={"enabled"},
)
def copy_file(source: str, destination: str, overwrite: bool = False) -> dict[str, Any]:
    """Copy a file or directory.

    Args:
        source: Source file or directory path.
        destination: Destination path.
        overwrite: Whether to overwrite if destination exists.

    Returns:
        dict: Operation status.
    """
    src = safe(source)
    dst = safe(destination)

    if not os.path.exists(src):
        return {"ok": False, "error": f"Source not found: {source}"}

    if os.path.exists(dst) and not overwrite:
        return {"ok": False, "error": f"Destination exists: {destination}"}

    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

    return {"ok": True, "source": source, "destination": destination}


@mcp.tool(
    name="move_file",
    description="Move a file or directory to a new location.",
    tags={"enabled"},
)
def move_file(source: str, destination: str, overwrite: bool = False) -> dict[str, Any]:
    """Move a file or directory.

    Args:
        source: Source file or directory path.
        destination: Destination path.
        overwrite: Whether to overwrite if destination exists.

    Returns:
        dict: Operation status.
    """
    src = safe(source)
    dst = safe(destination)

    if not os.path.exists(src):
        return {"ok": False, "error": f"Source not found: {source}"}

    if os.path.exists(dst) and not overwrite:
        return {"ok": False, "error": f"Destination exists: {destination}"}

    if os.path.exists(dst):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        else:
            os.remove(dst)

    shutil.move(src, dst)
    return {"ok": True, "source": source, "destination": destination}


@mcp.tool(
    name="delete_file",
    description="Delete a file or directory.",
    tags={"enabled"},
)
def delete_file(path: str) -> dict[str, Any]:
    """Delete a file or directory.

    Args:
        path: Path to delete.

    Returns:
        dict: Operation status.
    """
    full = safe(path)

    if not os.path.exists(full):
        return {"ok": False, "error": f"Path not found: {path}"}

    if os.path.isdir(full):
        shutil.rmtree(full)
    else:
        os.remove(full)

    return {"ok": True, "path": path}


@mcp.tool(
    name="create_directory",
    description="Create a new directory.",
    tags={"enabled"},
)
def create_directory(path: str, parents: bool = True) -> dict[str, Any]:
    """Create a directory.

    Args:
        path: Path to create.
        parents: Create parent directories if needed.

    Returns:
        dict: Operation status.
    """
    full = safe(path)
    os.makedirs(full, parents=parents, exist_ok=True)
    return {"ok": True, "path": path}


@mcp.tool(
    name="search_files",
    description="Search for files matching a pattern in a directory tree.",
    tags={"enabled"},
)
def search_files(root: str, pattern: str, max_results: int = 100) -> dict[str, Any]:
    """Search for files matching a pattern.

    Args:
        root: Root directory to search.
        pattern: Glob pattern to match.
        max_results: Maximum number of results.

    Returns:
        dict: List of matching file paths.
    """
    root_full = safe(root)
    if not os.path.exists(root_full):
        return {"ok": False, "error": f"Directory not found: {root}"}

    root_path = Path(root_full)
    matches = list(root_path.glob(pattern))[:max_results]
    results = [{"path": os.path.relpath(m, ROOT), "is_file": m.is_file(), "is_dir": m.is_dir()} for m in matches]

    return {"ok": True, "pattern": pattern, "results": results, "count": len(results)}


@mcp.tool(
    name="exists",
    description="Check if a file or directory exists.",
    tags={"enabled"},
)
def exists(path: str) -> dict[str, Any]:
    """Check if a path exists.

    Args:
        path: Path to check.

    Returns:
        dict: Existence status with type info.
    """
    full = safe(path)
    exists = os.path.exists(full)
    return {
        "ok": True,
        "path": path,
        "exists": exists,
        "is_file": os.path.isfile(full) if exists else False,
        "is_dir": os.path.isdir(full) if exists else False,
    }


@mcp.tool(
    name="get_size",
    description="Get the total size of a file or directory.",
    tags={"enabled"},
)
def get_size(path: str) -> dict[str, Any]:
    """Get the size of a file or directory.

    Args:
        path: Path to measure.

    Returns:
        dict: Size information.
    """
    full = safe(path)
    if not os.path.exists(full):
        return {"ok": False, "error": f"Path not found: {path}"}

    if os.path.isfile(full):
        size = os.path.getsize(full)
    else:
        size = sum(f.stat().st_size for f in Path(full).rglob("*") if f.is_file())

    return {
        "ok": True,
        "path": path,
        "size_bytes": size,
        "size_readable": _format_size(size),
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8005, stateless_http=True)
