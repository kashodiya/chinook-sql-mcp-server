# MCP SQL Demo

## Use it with Open WebUI
- Ensure Open WebUI is installed and running
- Do Admin Settings -> Tools -> Click + sign
    - Enter URL: http://host.docker.internal:8000
    - Make it public
    - Save
- New chat
- Refresh browser page
- Click + sign in message box
- Select tool
- Ask: Count albums

## How to run using STDIO
uvx mcpo --port 8000 -- uv run sql_mcp_server.py 

## How to run using SSE
- Run mcp server using sse (Note that we are running sse on 8001, see the last line in sql_mcp_server.py)
uv run sql_mcp_server.py 
- Run mcpo server
uvx mcpo --port 8000 --server-type "sse" -- http://127.0.0.1:8001/sse