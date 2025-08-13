
def format_table_cell(cell_text: str, is_first_row: bool):  
  if is_first_row:
    return f"<th style='border: 2px solid #006fbf;border-radius: 5px;padding:5px;background:#006fbf4d;'>{cell_text.strip()}</th>"
  
  return f"<td>{cell_text.strip()}</td>"

def format_first_cell_row(cell_text):
  return f"<tr>{cell_text}"

def format_last_cell_row(cell_text):
  return f"{cell_text}</tr>"