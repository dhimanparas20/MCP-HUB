# 🤖 MCP Hub - Your All-Powerful AI Agent Rig

<div align="center">

[![Docker](https://img.shields.io/docker/pulls/mcp-hub/mcp-hub?style=flat&color=blue)](https://hub.docker.com/r/mcp-hub/mcp-hub)
[![Python](https://img.shields.io/badge/python-3.13+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A universal AI agent platform that connects LLMs to databases, filesystems, downloads, web search, and more - all through natural language!**

</div>

---

## 🌟 What is MCP Hub?

MCP Hub is a **powerful AI agent framework** that gives your LLM (like GPT-4o, Gemini, Groq, etc.) the ability to interact with the real world through tools. Think of it as giving your AI "hands" to:

| Capability | What It Does |
|------------|---------------|
| 🗄️ **SQLite Database** | Create tables, run queries, insert/update/delete data |
| 📁 **File System** | Read, write, copy, move, delete files and folders |
| ⬇️ **Downloader** | Download files from any URL automatically |
| 🔍 **Web Search** | Search DuckDuckGo for current information |
| 🌐 **Web Fetch** | Fetch and summarize any webpage |
| 🐙 **Git Operations** | Run git commands (status, commit, branch, etc.) |
| ⏰ **Time Zones** | Get current time for any timezone |
| 📄 **Document Indexing** | Index PDFs, markdown, text files and search them with AI |
| 📧 **Email Sending** | Send emails via SMTP (queued for reliability) |
| ⏳ **Task Scheduling** | Schedule any task to run after a delay or at a specific time |

### 💡 Example Conversations

```
You: "Create a table called users with columns name, age, email"
AI:  ✓ Created table 'users' with columns: name (TEXT), age (INTEGER), email (TEXT)

You: "Show me all files in the datastore folder"
AI:  📁 Files in datastore:
     ├── downloads/
     ├── sqlite_ops.db
     └── uploads/

You: "Download this PDF https://example.com/report.pdf"
AI:  ⬇️ Downloaded successfully to ./datastore/downloads/report.pdf

You: "Send an email to boss@company.com saying project is complete"
AI:  ✓ Email queued! Job ID: abc-123-xyz
```

---

## 🚀 Quick Start (5 Minutes!)

### Step 1: Clone & Setup

```bash
git clone https://github.com/your-repo/sqlite-mcp.git
cd sqlite-mcp
```

### Step 2: Create Your `.env` File

Create a file named `.env` in the project root:

```bash
# ============================================
# 🎯 REQUIRED: Choose Your AI Provider
# ============================================
# Options: openai, google, openrouter, groq
MODEL_PROVIDER=openai

# Get your API key from the provider's website
OPENAI_API_KEY=sk-your-actual-key-here

# Optional: Specify model (defaults provided if not set)
OPENAI_MODEL=gpt-4o
MODEL_TEMPERATURE=0.5
MAX_TOKENS=1500

# ============================================
# 📧 Email (Optional - for send_email_task)
# ============================================
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# ============================================
# 📄 Document Search (Optional)
# ============================================
PAGE_INDEX_API_KEY=your-pageindex-key
```

### Step 3: Start Everything with Docker! 🐳

```bash
# This starts ALL services automatically:
# - Redis/Valkey (for task queue)
# - SQLite MCP Server (port 8000)
# - Filesystem MCP Server (port 8005)  
# - Downloader MCP Server (port 8010)
# - Huey Worker (background task processor)
# - FastAPI Web App (port 8001)

docker compose up
```

### Step 4: Open the Web App! 🌐

Once running, open your browser to:

```
http://localhost:8001
```

That's it! You're ready to chat with your AI agent!

---

## 📁 Project Structure

```
sqlite-mcp/
├── 📄 app.py                    # 🎯 Main entry point - starts the chat!
├── 🐳 compose.yml               # Docker configuration (start here!)
├── 🐋 Dockerfile                # Container image definition
├── 📦 pyproject.toml            # Python dependencies
├── 🌿 .env                      # YOUR API keys go here!
│
├── 🌐 mcps/                     # MCP Servers (built-in tools)
│   ├── mcp_server.py           # 🗄️ SQLite server (port 8000)
│   ├── mcp_server2.py          # 📁 Filesystem server (port 8005)
│   ├── mcp_server3.py         # ⬇️ Downloader server (port 8010)
│   └── __init__.py             # MCP server configuration
│
├── 🧠 modules/                  # Core AI modules
│   ├── tools.py                # LangChain tools (background tasks)
│   ├── agent_utils.py          # LLM connection factory
│   ├── logger.py              # Logging utilities
│   ├── vectorless.py          # Document indexing logic
│   └── system_prompts/        # AI instructions (how to use tools)
│
├── ⏳ tasks/                    # Background task system (Huey)
│   ├── tasks.py               # Task definitions (email, index, etc.)
│   └── __init__.py           # Task exports
│
├── 💾 datastore/               # Data storage
│   ├── sqlite_ops.db          # SQLite database
│   └── downloads/             # Downloaded files go here
│
├── 🌐 templates/              # Web UI templates (FastAPI)
├── 🤖 huey_consumer.py        # Background worker script
└── 📖 README.md               # You are here!
```

---

## 🔧 How to Configure

### Supported AI Providers

| Provider | Environment Variable | Example Models |
|----------|---------------------|----------------|
| **OpenAI** | `OPENAI_API_KEY` | gpt-4o, gpt-4o-mini, gpt-4-turbo |
| **Google** | `GOOGLE_API_KEY` | gemini-2.0-flash, gemini-pro |
| **Groq** | `GROQ_API_KEY` | llama-3.3-70b-versatile, mixtral-8x7b |
| **OpenRouter** | `OPEN_ROUTER_API_KEY` | x-ai/grok-4.1-fast, anthropic/claude-3 |

### Example Configurations

```bash
# Option 1: OpenAI (most popular)
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Option 2: Groq (free, fast!)
MODEL_PROVIDER=groq
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.3-70b-versatile

# Option 3: Google Gemini
MODEL_PROVIDER=google
GOOGLE_API_KEY=AI...
GOOGLE_MODEL=gemini-2.0-flash
```

---

## 🛠️ Adding or Modifying MCP Servers

MCP Servers are defined in `mcps/__init__.py`. Here's how to add new ones:

### Method 1: HTTP-based Server

```python
MCP_TOOLS = {
    # Add new HTTP server
    "my-new-server": {
        "url": "http://127.0.0.1:9000/mcp/",
        "transport": "streamable-http",
    },
}
```

### Method 2: STDIO-based Server (uvx)

```python
MCP_TOOLS = {
    # Add new uvx-based server
    "my-uvx-server": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "package-name"],
    },
}
```

### Method 3: Add Custom LangChain Tool

Edit `modules/tools.py`:

```python
from langchain.tools import tool

@tool("my_awesome_tool")
def my_awesome_tool(param: str) -> dict:
    """Description that tells the AI when to use this tool."""
    # Your code here
    return {"result": "success"}
```

Then add it to `get_vectorless_tools()` function.

---

## 🐳 Docker Compose Explained

```yaml
Services Started:
├── valkey       # Redis for task queue (port 6379)
├── mcp_sql      # SQLite MCP Server (port 8000)
├── mcp_fs       # Filesystem MCP Server (port 8005)
├── mcp_downloader # Downloader MCP Server (port 8010)
├── huey         # Background task worker
└── app          # FastAPI web app (port 8001)
```

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

# View running containers
docker compose ps

# Rebuild containers
docker compose build --no-cache
```

---

## 🎯 Where to Access

| Service | URL | Description |
|---------|-----|-------------|
| **Web App** | http://localhost:8001 | Main chat interface |
| **API Docs** | http://localhost:8001/docs | FastAPI Swagger UI |
| **SQLite** | http://localhost:8000 | MCP SQLite server |
| **Filesystem** | http://localhost:8005 | MCP Filesystem server |
| **Downloader** | http://localhost:8010 | MCP Downloader server |

---

## 💪 How Powerful Is This?

This is a **complete AI agent platform** that can:

1. **Build full applications** - Create databases, write code, manage files
2. **Automate workflows** - Schedule emails, downloads, document processing
3. **Research** - Search the web, fetch pages, index documents for AI search
4. **DevOps** - Run git commands, manage files, monitor systems
5. **Personal assistant** - Send emails, schedule tasks, manage your data

The best part? You just speak in natural language and the AI figures out which tools to use!

---

## 🔒 Security Notes

- **NEVER** commit your `.env` file to git - it's in `.gitignore`
- Store API keys securely
- The Docker container runs in an isolated network
- Database is stored locally in `datastore/`

---

## 🤔 Troubleshooting

### "Connection refused" errors
```bash
# Make sure all containers are running
docker compose ps

# Check logs for specific service
docker compose logs mcp_sql
```

### "API key not found"
```bash
# Verify your .env file exists
cat .env

# Restart containers after adding keys
docker compose restart
```

### "Tool not found"
- Check the tool is registered in `mcps/__init__.py` or `modules/tools.py`
- Rebuild: `docker compose build`
- Restart: `docker compose down && docker compose up`

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

**Made with ❤️ using FastMCP, LangChain, and FastAPI**