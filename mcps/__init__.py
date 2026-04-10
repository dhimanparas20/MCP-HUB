import os
from dotenv import load_dotenv

load_dotenv()

MCP_TOOLS = {
    "sqlite-local": {
        "url": "http://sql_mcp:8000/mcp/",
        "transport": "streamable-http",
    },
    "custom-fs": {
        "url": "http://fs_mcp:8005/mcp",
        "transport": "streamable-http",
    },
    "downloader": {
        "url": "http://downloader_mcp:8010/mcp",
        "transport": "streamable-http",
    },
    "ddg-search": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "duckduckgo-mcp-server"],
        "env": {
            "DDG_SAFE_SEARCH": "MODERATE",
            "DDG_REGION": "in-en",
        },
    },
    "fetch": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "mcp-server-fetch"],
    },
    "time": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "mcp-server-time"],
    },
    "url-downloader": {
        "command": "uv",
        "transport": "stdio",
        "args": ["run", "mcp-url-downloader", "--path", "/home/paras/Downloads/mcp_downloads"],
        "env": {"DEFAULT_OUTPUT_DIR": "/home/paras/Downloads/mcp_downloads"},
    },
    "pageindex": {
        "transport": "http",
        "url": "https://api.pageindex.ai/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv("PAGE_INDEX_API_KEY")}"},
    },
}
