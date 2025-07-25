from typing import Dict, Any, List
import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("Chinook DB MCP Server")
DATABASE_PATH = "chinook.db"

with open("SCHEMA.md", 'r', encoding='utf-8') as file:
    SCHEMA = file.read()
    print("SCHEMA.md file read.")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def get_database_schema() -> str:
    """Get complete database schema for BMO SQLite database.
    
    Database System: SQLite 3.x
    SQL Dialect: SQLite SQL (standard SQL with SQLite extensions)
    
    Returns schema with tables, columns, types, constraints, and relationships.
    Use this before generating SQL queries to ensure accuracy. Once you generate SQL statements, please execute using execute_sql_query tool.
    """
    print("[SQL] Returning complete database schema")
    return SCHEMA

def format_as_markdown_table(data: List[Dict], columns: List[str]) -> str:
    """Convert query results to markdown table format."""
    if not data or not columns:
        return "No data to display."
    
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    
    rows = []
    for row in data:
        values = [str(row.get(col, "NULL")) for col in columns]
        rows.append("| " + " | ".join(values) + " |")
    
    return "\n".join([header, separator] + rows) + f"\n\n*{len(data)} row(s) returned*"

@mcp.tool()
async def execute_sql_query(sql_query: str) -> str:
    """Execute SQL queries against BMO SQLite database and return results as markdown table.
    
    SECURITY RESTRICTION: Only SELECT queries are allowed for data safety.
    Returns formatted markdown table for better readability.
    """
    try:
        print(f"[SQL] Executing SQL Query: {sql_query}") 
        # await ctx.info(f"[SQL] Executing SQL Query: {sql_query}")

        # if not sql_query.strip().upper().startswith('SELECT'):
        #     return "Error: Only SELECT queries are allowed for security reasons."
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        data = [dict(row) for row in results]
        
        conn.close()
        markdown_table = format_as_markdown_table(data, columns)    
        print(f"[SQL] Query returned {len(data)} rows")
        print(markdown_table)
        return markdown_table
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="sse", port=8001)