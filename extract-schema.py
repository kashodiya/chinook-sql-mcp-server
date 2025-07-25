import sqlite3

def extract_schema():
    conn = sqlite3.connect('chinook.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    schema_md = "# Database Schema\n\n"
    
    for table in tables:
        table_name = table[0]
        schema_md += f"## {table_name}\n\n"
        
        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        schema_md += "| Column | Type | Not Null | Default | Primary Key |\n"
        schema_md += "|--------|------|----------|---------|-------------|\n"
        
        for col in columns:
            cid, name, type_, not_null, default, pk = col
            schema_md += f"| {name} | {type_} | {'Yes' if not_null else 'No'} | {default or 'NULL'} | {'Yes' if pk else 'No'} |\n"
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fks = cursor.fetchall()
        
        if fks:
            schema_md += "\n**Foreign Keys:**\n"
            for fk in fks:
                schema_md += f"- {fk[3]} -> {fk[2]}.{fk[4]}\n"
        
        schema_md += "\n"
    
    conn.close()
    
    with open('SCHEMA.md', 'w', encoding='utf-8') as f:
        f.write(schema_md)

if __name__ == "__main__":
    extract_schema()