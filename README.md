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

## How to run
uvx mcpo --port 8000 -- uv run sql_mcp_server.py 