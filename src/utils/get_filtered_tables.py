from docx.table import Table

def get_filtered_tables(tables: list[Table]):
  filtered_tables = []

  for table in tables:
    rows = []
    texts = [
        cell.text.strip() for row in table.rows for cell in row.cells if cell.text.strip()
    ]
    
    for text in texts:
      if text in rows:
        continue      
      rows.append(text)    

    filtered_tables += rows
  return filtered_tables