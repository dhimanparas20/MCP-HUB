# 🤖 MCP Hub - Universal AI Agent Platform

<div align="center">

[![Docker](https://img.shields.io/docker/pulls/mcp-hub/mcp-hub?style=flat&color=blue)](https://hub.docker.com/r/mcp-hub/mcp-hub)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A powerful AI agent platform that connects LLMs to databases, filesystems, downloads, web search, document indexing, emails, and more - all through natural language!**

</div>

---

## ✨ What is MCP Hub?

MCP Hub is an **AI agent framework** that gives your LLM (GPT-4o, Gemini, Groq, etc.) the ability to interact with the real world through tools. Think of it as giving your AI "hands" to:

| Capability | Description |
|------------|-------------|
| 🗄️ **SQLite Database** | Create tables, run queries, insert/update/delete data |
| 📁 **File System** | Read, write, copy, move, delete files and folders |
| ⬇️ **Downloader** | Download files from any URL automatically |
| 🔍 **Web Search** | Search DuckDuckGo for current information |
| 🌐 **Web Fetch** | Fetch and summarize any webpage |
| ⏰ **Time Zones** | Get current time for any timezone |
| 📄 **Document Indexing** | Index PDFs, markdown, text files and search them with AI |
| 📧 **Email** | Send emails via SMTP (queued for reliability) |
| 🌤️ **Weather** | Get weather information for any location |
| ⏳ **Task Scheduling** | Schedule any task to run after a delay or at a specific time |

### 💡 Example Conversations

```
You: "Create a table called users with columns name, age, email"
AI:  Created table 'users' with columns: name (TEXT), age (INTEGER), email (TEXT)

You: "Show me all files in the datastore folder"
AI:  Files in datastore:
     ├── downloads/
     ├── sqlite_ops.db
     └── uploads/

You: "Download this PDF https://example.com/report.pdf"
AI:  Downloaded successfully to ./datastore/downloads/report.pdf

You: "Send an email to boss@company.com saying project is complete"
AI:  Email queued! Job ID: abc-123-xyz
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

### Step 1: Clone & Setup

```bash
git clone https://github.com/your-repo/mcp-hub.git
cd mcp-hub
```

### Step 2: Create Your `.env` File

Copy the sample and configure:

```bash
cp .env.sample .env
```

Edit `.env` with your API keys:

```bash
# REQUIRED: Choose Your AI Provider (openai, google, openrouter, groq)
MODEL_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o

# GroQ (free, fast alternative)
# MODEL_PROVIDER=groq
# GROQ_API_KEY=gsk_your-key-here

# Google Gemini
# MODEL_PROVIDER=google
# GOOGLE_API_KEY=your-key-here

# OpenRouter (access to many models)
# MODEL_PROVIDER=openrouter
# OPEN_ROUTER_API_KEY=your-key-here

# PageIndex (for document search)
PAGE_INDEX_API_KEY=your-pageindex-key

# Email (optional - for send_email_task)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis/Valkey
REDIS_URL=redis://:testpass@valkey:6379/0
```

### Step 3: Start with Docker

```bash
docker compose up
```

This starts all services:
- **Valkey** (Redis) - Task queue (port 6379)
- **SQLite MCP Server** - Database operations (port 8000)
- **Downloader MCP Server** - File downloads (port 8010)
- **Huey Worker** - Background task processor
- **FastAPI App** - Web interface (port 8001)

### Step 4: Open the Web App

```
http://localhost:8001
```

---

## 📁 Project Structure

```
mcp-hub/
├── app.py                    # FastAPI entry point
├── compose.yml               # Docker compose configuration
├── Dockerfile              # Container image definition
├── pyproject.toml           # Python dependencies
├── .env/.env.sample        # Environment configuration
│
├── mcps/                   # MCP Servers
│   ├── __init__.py         # MCP server configuration
│   ├── mcp_sql.py         # SQLite MCP server
│   ├── mcp_fs.py          # Filesystem MCP server
│   └── mcp_downloader.py # Downloader MCP server
│
├── modules/                 # Core AI modules
│   ├── __init__.py        # Module exports
│   ├── agent_mod.py       # MCP Agent orchestration
│   ├── agent_utils.py    # LLM factory
│   ├── tools.py          # LangChain tools
│   ├── logger.py         # Logging utilities
│   └── system_prompts/  # AI instructions
│
├── tasks/                  # Background tasks (Huey)
│   ├── __init__.py       # Task exports
│   └── tasks.py         # Task definitions
│
├── datastore/              # Data storage
│   ├── internal/         # Internal data (SQLite, history)
│   └── downloads/       # Downloaded files
│
└── templates/             # Web UI templates
```

---

## 🔧 Configuration

### Supported AI Providers

| Provider | Environment Variable | Notes |
|----------|-----------------|-------|
| **OpenAI** | `OPENAI_API_KEY` | Default - gpt-4o, gpt-4o-mini |
| **Google** | `GOOGLE_API_KEY` | gemini-2.5-flash |
| **Groq** | `GROQ_API_KEY` | Free, fast - llama-3.3-70b |
| **OpenRouter** | `OPEN_ROUTER_API_KEY` | Access to 100+ models |

### Model Configuration

```bash
MODEL_PROVIDER=openai        # Provider choice
MODEL_TEMPERATURE=0.4        # Creativity (0-1)
MAX_TOKENS=1500              # Max response length
OPENAI_MODEL=gpt-4o          # Model name
```

---

## 🛠️ Available Tools

### MCP Servers (via langchain-mcp-adapters)

| Tool | Description |
|------|-------------|
| `sqlite-local` | SQLite operations - CRUD on local database |
| `downloader` | Download files from URLs |
| `ddg-search` | DuckDuckGo web search |
| `fetch` | Fetch web page content |
| `time` | Get time for timezones |
| `url-downloader` | Download to custom directory |
| `pageindex` | Query indexed documents |

### LangChain Tools (Background Tasks)

| Tool | Description |
|------|-------------|
| `index_files` | Index local files to PageIndex |
| `index_urls` | Index remote URLs to PageIndex |
| `send_email_task` | Send email via SMTP |
| `schedule_task` | Schedule tasks with delay/eta |
| `get_background_task_status` | Check task status by job ID |
| `get_all_tasks` | List all queued tasks |
| `get_system_datetime` | Get current system time |
| `weather_tool` | Get weather info |
| `sleep` | Queue sleep task |

### File Management Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Write content to file |
| `copy_file` | Copy files |
| `move_file` | Move files |
| `delete_file` | Delete files |
| `list_directory` | List directory contents |
| `make_directory` | Create directories |
| `move_directory` | Move directories |

---

## 🐳 Docker Services

| Service | Port | Description |
|--------|------|-------------|
| valkey | 6379 | Redis task queue |
| mcp_sql | 8000 | SQLite MCP server |
| mcp_downloader | 8010 | Downloader MCP server |
| huey | - | Background worker |
| app | 8001 | FastAPI web app |

### Useful Docker Commands

```bash
# Start everything
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Rebuild containers
docker compose build --no-cache
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/ping` | GET | Health check |
| `/api/chat` | POST | Send chat message |
| `/api/history` | GET | Get chat history |
| `/api/clear` | POST | Clear history |
| `/api/health` | GET | Detailed health |
| `/docs` | GET | Swagger UI |

---

## 🧩 Adding Custom MCP Servers

MCP servers are configured in `mcps/__init__.py`:

### HTTP-based Server

```python
MCP_TOOLS = {
    "my-server": {
        "url": "http://127.0.0.1:9000/mcp/",
        "transport": "streamable-http",
    },
}
```

### STDIO-based Server (uv)

```python
MCP_TOOLS = {
    "my-uvx-server": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "package-name"],
    },
}
```

### Custom LangChain Tool

Edit `modules/tools.py`:

```python
from langchain.tools import tool

@tool("my_awesome_tool")
def my_awesome_tool(param: str) -> dict:
    """Description for the AI when to use this tool."""
    return {"result": "success"}
```

Add to `get_vectorless_tools()` in the same file.

---

## 🔒 Security Notes

- **NEVER** commit `.env` to git (it's in `.gitignore`)
- Store API keys securely
- The container runs in an isolated network
- Database stored locally in `datastore/`
- Use strong passwords for Redis in production

---

## 🤔 Troubleshooting

### "Connection refused" errors
```bash
# Check all containers running
docker compose ps

# Check logs for specific service
docker compose logs mcp_sql
```

### "API key not found"
```bash
# Verify .env file
cat .env

# Restart after adding keys
docker compose restart
```

### "Tool not found"
- Check tool in `mcps/__init__.py` or `modules/tools.py`
- Rebuild: `docker compose build`
- Restart: `docker compose down && docker compose up`

### "Redis connection failed"
- Check Valkey service: `docker compose logs valkey`
- Verify REDIS_URL in `.env`

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR!

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

---

**Built with ❤️ using FastMCP, LangChain, FastAPI, and Huey**