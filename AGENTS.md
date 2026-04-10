# AGENTS.md - AI Agent Guidelines

This document provides context for AI agents working on this codebase.

## Project Overview

**Project Name**: MCP Hub  
**Type**: CLI tool with embedded MCP servers  
**Core Functionality**: Universal MCP server connector with LLM-powered chat interface with built-in SQLite, Filesystem, Downloader, and Vectorless RAG (PageIndex) MCP servers  
**Status**: Production-ready

---

## Architecture

MCP Hub connects to multiple MCP servers and exposes their tools via LangChain agents:

```
app.py (Chat CLI)
       │
       ├── MultiServerMCPClient (mcps/__init__.py)
       │
       ├── Built-in MCP Servers:
       │   ├── mcps/mcp_server.py (SQLite - port 8000)
       │   ├── mcps/mcp_server2.py (Filesystem - port 8005)
       │   └── mcps/mcp_server3.py (Downloader - port 8010)
       │
       ├── External MCP Servers (uvx):
       │   ├── ddg-search (DuckDuckGo)
       │   ├── fetch (Web pages)
       │   ├── git (Git operations)
       │   ├── time (Timezones)
       │   └── url-downloader (Alternative downloader)
       │
       ├── LangChain Tools (modules/tools.py):
       │   ├── index_files
       │   ├── index_urls
       │   └── query_index
       │
       └── create_llm → LLM (OpenAI/Google/Groq/OpenRouter)
```

---

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main chat CLI with history management |
| `modules/__init__.py` | Exports `create_llm`, prompts, logger, get_logger |
| `mcps/__init__.py` | MCP_TOOLS configuration |
| `modules/agent_utils.py` | LLM factory for multiple providers |
| `modules/logger.py` | Colored logging setup (get_logger) |
| `modules/tools.py` | Vectorless RAG LangChain tools (@tool decorators) |
| `modules/vectorless.py` | Document indexing logic with ThreadPoolExecutor |
| `modules/system_prompts/` | Agent system prompts |
| `mcps/mcp_server.py` | SQLite MCP server (FastMCP) - port 8000 |
| `mcps/mcp_server2.py` | Filesystem MCP server (FastMCP) - port 8005 |
| `mcps/mcp_server3.py` | Downloader MCP server (FastMCP) - port 8010 |

---

## MCP Server Configuration

**File**: `mcps/__init__.py`

Servers are defined in `MCP_TOOLS` dict with these transport types:

### 1. HTTP-based (streamable-http)
```python
"server-name": {
    "url": "http://127.0.0.1:8000/mcp/",
    "transport": "streamable-http",
}
```

### 2. STDIO-based (uv)
```python
"server-name": {
    "command": "uv",
    "transport": "stdio",
    "args": ["run", "package-name"],
    "env": {"KEY": "value"},  # optional
}
```

---

## Default Configured Servers

```python
MCP_TOOLS = {
    "sqlite-local": {
        "url": "http://127.0.0.1:8000/mcp/",
        "transport": "streamable-http",
    },
    "custom-fs": {
        "url": "http://127.0.0.1:8005/mcp",
        "transport": "streamable-http",
    },
    "downloader": {
        "url": "http://127.0.0.1:8010/mcp",
        "transport": "streamable-http",
    },
    "ddg-search": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "duckduckgo-mcp-server"],
    },
    "fetch": {...},
    "git": {...},
    "time": {...},
    "url-downloader": {...},
    "pageindex": {...},
}
```

---

## LLM Providers

**File**: `modules/agent_utils.py`

Supported providers via `MODEL_REGISTRY`:

| Provider | Env Vars | Config |
|----------|----------|--------|
| `openai` | `OPENAI_API_KEY`, `OPENAI_MODEL` | langchain_openai.ChatOpenAI |
| `google` | `GOOGLE_API_KEY`, `GOOGLE_MODEL` | langchain_google_genai.ChatGoogleGenerativeAI |
| `openrouter` | `OPEN_ROUTER_API_KEY`, `OPEN_ROUTER_CHAT_MODEL` | langchain_openrouter.ChatOpenRouter |
| `groq` | `GROQ_API_KEY`, `GROQ_MODEL` | langchain_groq.ChatGroq |

### Using `create_llm`

```python
from modules import create_llm

llm = create_llm(
    model_provider="openai",      # or "google", "openrouter", "groq"
    model_name="gpt-4o",
    model_temperature=0.5,
    max_tokens=1500,
)
```

---

## Built-in MCP Servers

### SQLite Server (mcps/mcp_server.py)

Runs on port 8000. Database: `./datastore/sqlite_ops.db`

**Tools**:
- `list_tables` - List all tables
- `table_info(table_name)` - Get schema
- `create_table(table_name, columns, if_not_exists, primary_key, unique)` - Create table
- `insert_rows(data, table_name)` - Insert rows
- `select_rows(table_name, columns, where, order_by, limit, offset, distinct)` - Query rows
- `select_one_row(table_name, columns, where, order_by)` - Query single row
- `update_rows(table_name, data, where)` - Update rows
- `delete_rows(table_name, where)` - Delete rows
- `upsert_row(table_name, data, conflict_columns, update_columns)` - Upsert
- `count_rows(table_name, where)` - Count rows
- `active_database()` - Get current DB path
- `delete_table(table_name)` - Drop table
- `flush_database()` - Drop all tables
- `rename_table(table_name, new_table_name)` - Rename table
- `execute_sql(sql, params)` - Raw SQL
- `create_index(index_name, table_name, columns, unique, if_not_exists)` - Create index
- `list_indexes()` - List indexes
- `vacuum_database()` - Optimize DB

### Filesystem Server (mcps/mcp_server2.py)

Runs on port 8005. Root: Project directory

**Tools**:
- `list_directory(path, pattern, include_hidden)` - List directory
- `get_file_info(path)` - File details
- `read_file(path, max_size)` - Read content
- `write_file(path, content, create_dirs)` - Write content
- `create_file(path, content, create_dirs)` - Create file
- `copy_file(source, destination, overwrite)` - Copy
- `move_file(source, destination, overwrite)` - Move
- `delete_file(path)` - Delete
- `create_directory(path, parents)` - Create directory
- `search_files(root, pattern, max_results)` - Glob search
- `exists(path)` - Check existence
- `get_size(path)` - Get size
- `get_cwd()` - Get working directory
- `list_dir(path)` - List directory
- `path_info(path)` - Path details
- `get_pwd()` - Print working directory
- `tree(path, max_depth, include_hidden)` - Directory tree

### Downloader Server (mcps/mcp_server3.py)

Runs on port 8010. Download directory: `./datastore/downloads`

**Tools**:
- `download_file(url, custom_filename, timeout)` - Download single file
- `download_batch(urls, timeout, stop_on_error)` - Download multiple files
- `list_downloads()` - List downloaded files
- `get_download_info(filename)` - Get file details
- `delete_download(filename)` - Delete a file
- `delete_all_downloads()` - Clear all downloads
- `get_download_dir()` - Get download directory path
- `check_url(url, timeout)` - Check URL accessibility

**Environment Variables**:
- `DOWNLOAD_MCP_DIR` - Custom download directory (default: ./datastore/downloads)
- `FASTMCP3_PORT` - Server port (default: 8010)

---

## External MCP Tools (uvx-based)

These are configured in `mcps/__init__.py`:

| Tool | Package | Description |
|------|---------|-------------|
| `ddg-search` | duckduckgo-mcp-server | Web search via DuckDuckGo |
| `fetch` | mcp-server-fetch | Fetch and summarize web pages |
| `git` | mcp-server-git | Git repository operations |
| `time` | mcp-server-time | Get current time for timezones |
| `url-downloader` | mcp-url-downloader | Alternative file downloader |

---

## Vectorless RAG Tools (PageIndex)

**File**: `modules/tools.py` and `modules/vectorless.py`

Uses `@tool` decorator from langchain.tools. Supports both files and URLs, handles lists or strings, uses ThreadPoolExecutor with 10 workers.

### Tools (defined in modules/tools.py):

```python
@tool("index_files")
def index_files(file_paths: Union[str, List[str]], api_key: Optional[str] = None) -> str:
    """Index local files (pdf, md, txt, csv, etc.) to PageIndex for searching."""

@tool("index_urls")
def index_urls(urls: Union[str, List[str]], api_key: Optional[str] = None) -> str:
    """Index remote file URLs (pdf, md, txt, csv, etc.) to PageIndex."""

@tool("query_index")
def query_index(query: str, limit: int = 5, api_key: Optional[str] = None) -> str:
    """Query indexed documents from PageIndex to find relevant content."""
```

### Indexing Logic (modules/vectorless.py):

```python
def index_documents(
    sources: Union[str, List[str]],  # Accepts str or List[str]
    api_key: str,
    max_workers: int = 10,            # ThreadPool with 10 workers
    poll_interval: int = 5,
    timeout: int = 300,
) -> List[Dict[str, Any]]:
    """Index documents using ThreadPoolExecutor for parallel processing."""
```

**Environment Variable**: `PAGE_INDEX_API_KEY`

---

## Adding New LangChain Tools

In `modules/tools.py`, use the `@tool` decorator:

```python
from langchain.tools import tool

@tool("tool_name")
def my_tool(param: str) -> str:
    """Description of what the tool does."""
    return "result"

def get_vectorless_tools():
    return [index_files, index_urls, query_index, my_tool]
```

---

## System Prompts

**File**: `modules/system_prompts/`

Two prompts available:

1. `LOCAL_MCP_SQLITE3_PROMPT` - SQLite-focused (for database operations)
2. `GENERAL_PROMPT` - General purpose (for all tools including vectorless)

### Using Prompts

```python
from modules import LOCAL_MCP_SQLITE3_PROMPT, GENERAL_PROMPT

# Default is GENERAL_PROMPT
await agent.init(model_provider="openai", system_message=GENERAL_PROMPT)
```

---

## Chat History

**File**: `app.py`

- Stored in `chat_history.json` (JSON format)
- Keeps last 30 messages
- Loaded on startup, saved after each response
- Cleared on exit (`q`, `quit`, `exit`)
- Format: `[{"type": "human"/"ai", "data": {"content": "..."}}]`

### Message Classes

- `HumanMessage` - user input
- `AIMessage` - model response
- `SystemMessage` - system prompt

---

## Chat Client

**File**: `app.py`

### Components

- `MCPAgentModule` - main class managing agent, tools, history
- `self.tools` - MCP tools from MultiServerMCPClient
- `self.vectorless_tools` - LangChain tools from get_vectorless_tools()
- `self.all_tools` - Combined tools (tools + vectorless_tools)
- `_load_history()` - loads chat history from JSON
- `_save_history()` - saves to JSON (max 30 messages)
- `_clear_history()` - deletes history on exit
- `invoke_agent()` - non-streaming agent invocation
- `agent_stream()` - streaming agent invocation with reasoning

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MODEL_PROVIDER` | Yes | openai/google/openrouter/groq |
| `OPENAI_API_KEY` | If using OpenAI | OpenAI API key |
| `GOOGLE_API_KEY` | If using Google | Google AI API key |
| `OPEN_ROUTER_API_KEY` | If using OpenRouter | OpenRouter API key |
| `GROQ_API_KEY` | If using Groq | Groq API key |
| `PAGE_INDEX_API_KEY` | For vectorless RAG | PageIndex API key |
| `MODEL_TEMPERATURE` | No | Default: 0.5 |
| `MAX_TOKENS` | No | Default: 1500 |
| `DEFAULT_MCP_SERVER_URL` | No | Default SQLite server URL |
| `SQLITE_MCP_DB_PATH` | No | Default: ./datastore/sqlite_ops.db |
| `FASTMCP_HOST` | No | Default: 0.0.0.0 |
| `FASTMCP_PORT` | No | Default: 8000 |
| `FASTMCP2_PORT` | No | Default: 8005 |
| `FASTMCP3_PORT` | No | Default: 8010 |
| `DOWNLOAD_MCP_DIR` | No | Default: ./datastore/downloads |

---

## Running the Project

### Docker (Recommended)

```bash
docker compose up
```

Then in another terminal:

```bash
uv run app.py
```

### Manual

```bash
# Terminal 1 - SQLite server (port 8000)
uv run --frozen mcps.mcp_server

# Terminal 2 - Filesystem server (port 8005)
uv run --frozen mcps.mcp_server2

# Terminal 3 - Downloader server (port 8010)
uv run --frozen mcps.mcp_server3

# Terminal 4 - Chat CLI
uv run app.py
```

---

## Code Style

- Use type hints where possible
- Prefer async/await for I/O operations
- Use dataclasses for structured data
- Follow existing naming conventions
- Add docstrings to new functions
- Use `@tool` decorator for LangChain tools (not BaseTool class)
- Use `get_logger(__name__)` for logging in modules

---

## Future Enhancements

When expanding this codebase, consider:
- Web UI (FastAPI/Streamlit)
- Interactive MCP server discovery
- Vector store for long-term memory
- Tool result caching
- Request/response validation
- Rate limiting and retries