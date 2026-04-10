# MCP Hub - Complete Beginner's Guide

> A universal CLI for connecting to multiple MCP servers and interacting with them via natural language using LLMs.

## Table of Contents
1. [What is MCP Hub?](#what-is-mcp-hub)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Understanding the Architecture](#understanding-the-architecture)
4. [Configuration](#configuration)
5. [Built-in Servers & Tools Explained](#built-in-servers--tools-explained)
6. [Vectorless RAG (AI Search)](#vectorless-rag-ai-search)
7. [Adding/Removing Tools](#addingremoving-tools)
8. [Changing Models](#changing-models)
9. [How the App Works](#how-the-app-works)
10. [Troubleshooting](#troubleshooting)

---

## What is MCP Hub?

MCP Hub is a **Chat CLI** (Command Line Interface) that lets you talk to your computer using natural language. Think of it as having a smart assistant that can:

- **Query databases** (SQLite) by just asking
- **Manage files** (create, read, delete, search)
- **Download files** from URLs
- **Search the web** (DuckDuckGo)
- **Index and search documents** (PDF, Markdown, CSV, etc.) using AI
- **Run Git commands**
- **Get current time** for any timezone

Instead of writing SQL commands or terminal commands, you just type what you want in plain English!

### Example Usage

```
Enter Your Query: list all tables in the database
Enter Your Query: create a table users with name text age int email text
Enter Your Query: insert a user named Alice who is 25 years old
Enter Your Query: show me all files in the datastore folder
Enter Your Query: download this file https://example.com/data.csv
Enter Your Query: index this PDF file for searching
Enter Your Query: q
```

---

## Quick Start (5 Minutes)

### Step 1: Install

```bash
# Clone and enter the directory
git clone <your-repo>
cd sqlite-mcp

# Install dependencies
uv sync
```

### Step 2: Create Environment File

Create a `.env` file in the project root:

```bash
# REQUIRED: Choose your LLM provider
MODEL_PROVIDER=openai

# Your API key (get from respective provider's website)
OPENAI_API_KEY=sk-your-actual-key-here

# Optional: Specify model (defaults provided if not set)
OPENAI_MODEL=gpt-4o

# Optional settings
MODEL_TEMPERATURE=0.5
MAX_TOKENS=1500

# Vectorless RAG (if using document indexing)
PAGE_INDEX_API_KEY=your-pageindex-key
```

### Step 3: Run Everything

**Option A: Docker (Recommended)**
```bash
# Start everything with one command
docker compose up
```

Then open a NEW terminal and run:
```bash
uv run app.py
```

**Option B: Manual**
```bash
# Terminal 1 - Start SQLite database server (port 8000)
uv run --frozen mcps.mcp_server

# Terminal 2 - Start Filesystem server (port 8005)  
uv run --frozen mcps.mcp_server2

# Terminal 3 - Start Downloader server (port 8010)
uv run --frozen mcps.mcp_server3

# Terminal 4 - Start the chat app
uv run app.py
```

### Step 4: Start Chatting!

```
╭────────────────────────────────────────────────────────────╮
│                    MCP Hub v1.0                           │
╰────────────────────────────────────────────────────────────╯

Enter Your Query: list all tables
```

---

## Understanding the Architecture

Here's how everything fits together:

```
┌─────────────────────────────────────────────────────────────┐
│                      YOUR INPUT                             │
│            (Natural language query)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     app.py                                  │
│              (The Chat Interface)                           │
│                                                             │
│  - Takes your input                                         │
│  - Sends to LLM with tools                                  │
│  - Receives and displays response                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
┌─────────────────────┐  ┌─────────────────────┐
│   MCP Servers       │  │      LLM            │
│   (Your Tools)     │  │   (AI Brain)        │
│                     │  │                     │
│ - sqlite-local      │  │ - OpenAI            │
│ - custom-fs         │  │ - Google            │
│ - downloader       │  │ - Groq              │
│ - ddg-search      │  │ - OpenRouter        │
│ - index_tools     │  │                     │
│ - query_index    │  │                     │
└─────────────────────┘  └─────────────────────┘
```

### Key Components

| Component | What it does |
|-----------|--------------|
| **app.py** | The main chat interface - what you interact with |
| **MCP Servers** | Programs that expose tools (like database, file system, downloader) |
| **LLM (AI)** | The AI model that understands your request and decides which tools to use |
| **LangChain** | The "glue" that connects everything together |

---

## Configuration

### Environment Variables

Create a `.env` file with these options:

```bash
# ================= REQUIRED =================
# Choose one: openai, google, openrouter, groq
MODEL_PROVIDER=openai

# Your API key from the provider
OPENAI_API_KEY=sk-...  # for OpenAI
# GOOGLE_API_KEY=...   # for Google
# OPEN_ROUTER_API_KEY=...  # for OpenRouter
# GROQ_API_KEY=...     # for Groq

# ================= OPTIONAL =================
# Model settings
OPENAI_MODEL=gpt-4o
MODEL_TEMPERATURE=0.5
MAX_TOKENS=1500

# Vectorless RAG (PageIndex)
PAGE_INDEX_API_KEY=your-pageindex-key

# File downloads directory (optional)
DOWNLOAD_MCP_DIR=./datastore/downloads
```

### Supported LLM Providers

| Provider | API Key Env Var | Example Model |
|----------|-----------------|---------------|
| OpenAI | `OPENAI_API_KEY` | gpt-4o, gpt-4o-mini |
| Google | `GOOGLE_API_KEY` | gemini-2.0-flash |
| OpenRouter | `OPEN_ROUTER_API_KEY` | x-ai/grok-4.1-fast |
| Groq | `GROQ_API_KEY` | llama-3.3-70b-versatile |

---

## Built-in Servers & Tools Explained

### 1. SQLite Server (Port 8000) - `mcps/mcp_server.py`

This server gives you a **complete database** with these tools:

| Tool | What it does | Example |
|------|--------------|---------|
| `list_tables` | Show all tables in database | "show me all tables" |
| `table_info` | Show table structure | "what columns does users have?" |
| `create_table` | Create new table | "create table products with name text price float" |
| `insert_rows` | Add data | "insert into users name Alice age 30" |
| `select_rows` | Query data | "find all users over 25" |
| `select_one_row` | Query single row | "get the first user" |
| `update_rows` | Modify data | "update users set age 31 where name Alice" |
| `delete_rows` | Remove data | "delete users where age under 18" |
| `upsert_row` | Insert or update | "upsert user named Bob" |
| `count_rows` | Count records | "how many users are there?" |
| `execute_sql` | Run raw SQL | "execute SELECT * FROM users" |
| `delete_table` | Delete table | "drop table old_data" |
| `flush_database` | Delete all tables | "clear all tables" |
| `rename_table` | Rename table | "rename users to customers" |
| `create_index` | Create index | "create index on users email" |
| `list_indexes` | List indexes | "show all indexes" |
| `vacuum_database` | Optimize database | "optimize the database" |

**Database Location:** `./datastore/sqlite_ops.db`

**Start Command:** `uv run --frozen mcps.mcp_server`

---

### 2. Filesystem Server (Port 8005) - `mcps/mcp_server2.py`

This server lets you **manage files and folders**:

| Tool | What it does | Example |
|------|--------------|---------|
| `list_directory` | List folder contents | "list files in datastore" |
| `read_file` | Read file content | "read the README.md" |
| `write_file` | Create/update file | "write hello to test.txt" |
| `create_file` | Create new file | "create file notes.txt" |
| `delete_file` | Delete file/folder | "delete oldfile.txt" |
| `copy_file` | Copy file | "copy file.txt to backup.txt" |
| `move_file` | Move/rename | "move file to newfolder" |
| `create_directory` | Create folder | "create folder myproject" |
| `search_files` | Find files by pattern | "find all .py files" |
| `tree` | Show folder structure | "show directory tree" |
| `get_size` | Get file/folder size | "size of datastore" |
| `exists` | Check if path exists | "check if file exists" |

**Root Directory:** Project root

**Start Command:** `uv run --frozen mcps.mcp_server2`

---

### 3. Downloader Server (Port 8010) - `mcps/mcp_server3.py`

This server lets you **download files from URLs**:

| Tool | What it does | Example |
|------|--------------|---------|
| `download_file` | Download a single file | "download https://example.com/file.pdf" |
| `download_batch` | Download multiple files | "download these files: [url1, url2]" |
| `list_downloads` | List downloaded files | "show all downloaded files" |
| `get_download_info` | Get file details | "info about file.pdf" |
| `delete_download` | Delete a file | "delete file.pdf" |
| `delete_all_downloads` | Clear all downloads | "clear all downloads" |
| `get_download_dir` | Get download folder path | "where are downloads saved?" |
| `check_url` | Check URL accessibility | "check if this URL works" |

**Download Directory:** `./datastore/downloads`

**Start Command:** `uv run --frozen mcps.mcp_server3`

---

### 4. External MCP Tools (via uvx)

These come from the `mcps/__init__.py` configuration:

| Tool | What it does |
|------|--------------|
| `ddg-search` | Web search via DuckDuckGo |
| `fetch` | Fetch and summarize web pages |
| `git` | Git repository operations |
| `time` | Get current time for timezones |
| `url-downloader` | Alternative downloader (uvx-based) |

---

### 5. Vectorless RAG (PageIndex) - `modules/tools.py`

**AI-powered document search**. Index documents (PDF, MD, TXT, CSV) and search with natural language:

| Tool | What it does | Example |
|------|--------------|---------|
| `index_files` | Index local files | "index all PDFs in ./docs" |
| `index_urls` | Index remote files | "index https://example.com/doc.pdf" |
| `query_index` | Search indexed docs | "find mention of..." |

**How it works:**
1. Index documents → Processed by PageIndex
2. Query with natural language → AI searches content
3. Get relevant results with context

**Prerequisites:**
```bash
pip install pageindex
# And set PAGE_INDEX_API_KEY in .env
```

---

## Adding/Removing Tools

### Method 1: Add MCP Servers (`mcps/__init__.py`)

Edit to add more MCP servers:

```python
MCP_TOOLS = {
    # Existing servers...
    
    # NEW: Add a new HTTP-based server
    "my-server": {
        "url": "http://127.0.0.1:9000/mcp/",
        "transport": "streamable-http",
    },
    
    # NEW: Add a uvx-based server
    "duckduckgo": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "duckduckgo-mcp-server"],
    },
}
```

### Method 2: Add LangChain Tools (`modules/tools.py`)

Add new tools using the `@tool` decorator:

```python
from langchain.tools import tool

@tool("my_tool_name")
def my_tool(param: str) -> str:
    """Description for the AI."""
    # Your code here
    return "result"

# Add to the list
def get_vectorless_tools():
    return [index_files, index_urls, query_index, my_tool]
```

### Method 3: Remove Tools

Simply remove or comment out entries in:
- `mcps/__init__.py` - Remove MCP servers
- `modules/tools.py` - Remove functions from the list

---

## Changing Models

### Option 1: Change via .env

```bash
# OpenAI
MODEL_PROVIDER=openai
OPENAI_MODEL=gpt-4o

# OR Google
MODEL_PROVIDER=google
GOOGLE_MODEL=gemini-2.0-flash

# OR Groq (fast and free!)
MODEL_PROVIDER=groq
GROQ_MODEL=llama-3.3-70b-versatile

# OR OpenRouter (many models)
MODEL_PROVIDER=openrouter
OPEN_ROUTER_CHAT_MODEL=x-ai/grok-4.1-fast
```

### Option 2: Change in Code (app.py)

Find this section in `app.py`:
```python
await agent.init(
    model_provider="openai",    # Change here
    model_name="gpt-4o",      # And here
    system_message=GENERAL_PROMPT
)
```

---

## How the App Works

### Flow Diagram

```
1. You type: "list all tables"
     │
     ▼
2. app.py creates a HumanMessage
     │
     ▼
3. System adds system_prompt (instructions)
     │
     ▼
4. LangChain agent gets your message + available tools
     │
     ▼
5. LLM decides: "I should use list_tables tool"
     │
     ▼
6. LangChain calls the tool
     │
     ▼
7. Tool returns result (table names)
     │
     ▼
8. LLM formats response for you
     │
     ▼
9. app.py displays the answer
```

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main chat interface |
| `modules/agent_utils.py` | Creates LLM connections |
| `mcps/__init__.py` | Defines which MCP servers to connect |
| `modules/tools.py` | LangChain tools (index_files, etc.) |
| `modules/vectorless.py` | Document indexing logic |
| `modules/system_prompts/` | Instructions for the AI |
| `mcps/mcp_server.py` | SQLite database server (port 8000) |
| `mcps/mcp_server2.py` | Filesystem server (port 8005) |
| `mcps/mcp_server3.py` | Downloader server (port 8010) |

---

## Troubleshooting

### "No API key" Error
Make sure your `.env` file has the correct API key for your chosen provider.

### "Connection refused" Error
Make sure MCP servers are running:
```bash
# Check if servers are running
docker compose ps  # if using Docker
```

### "Module not found" Error
```bash
# Reinstall dependencies
uv sync
```

### "Tool not found" Error
The tool might not be registered. Check:
1. `mcps/__init__.py` for MCP servers
2. `modules/tools.py` for LangChain tools

---

## Project Structure

```
sqlite-mcp/
├── app.py                     # Main chat CLI (START HERE)
├── pyproject.toml             # Dependencies
├── .env                       # Your API keys
├── compose.yml                # Docker setup
├── datastore/                 # Data storage
│   ├── sqlite_ops.db          # SQLite database
│   └── downloads/              # Downloaded files
├── modules/
│   ├── __init__.py            # Exports
│   ├── agent_utils.py         # LLM setup
│   ├── logger.py             # Logging utilities
│   ├── tools.py               # Vectorless RAG LangChain tools
│   ├── vectorless.py         # Document indexing logic
│   ├── system_prompts/        # AI instructions
│   └── sqlite3/              # SQLite utilities
├── mcps/                     # MCP servers
│   ├── __init__.py           # MCP_TOOLS configuration
│   ├── mcp_server.py         # SQLite server (port 8000)
│   ├── mcp_server2.py        # Filesystem server (port 8005)
│   └── mcp_server3.py        # Downloader server (port 8010)
└── chat_history.json          # Your chat history
```

---

## Common Questions

**Q: Do I need all three MCP servers running?**
A: For basic usage, yes. But you can modify `mcps/__init__.py` to only include the servers you need.

**Q: Can I use this without Docker?**
A: Yes! Use the "Manual" method in Quick Start section.

**Q: How do I add more tools?**
A: See "Adding/Removing Tools" section above.

**Q: What's the difference between MCP tools and LangChain tools?**
A: MCP tools come from external servers. LangChain tools are defined directly in Python. Both work the same way in the chat!

**Q: How does Vectorless RAG work?**
A: It uses PageIndex to index documents. You "upload" files, then can search them using natural language.

**Q: What external tools are available?**
A: DDG search, fetch (web pages), git, time, url-downloader - all configured in `mcps/__init__.py`

---

## License

MIT