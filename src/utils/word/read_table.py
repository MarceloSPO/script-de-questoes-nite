from docx.table import Table
from docx.document import Document
from docx.oxml.table import CT_Tbl
from utils.word.get_expressions import get_text_expressions

from utils.html.format_table import format_table_cell

def read_table(element: CT_Tbl, doc: Document) -> str:
  table = Table(element, doc)  
  table_html = ""

  colspan_size = 0
  is_first_row = True

  for row in table.rows:
    current_row = []
    
    for cell in row.cells:
      formatted_cell = format_table_cell(get_text_expressions(cell), is_first_row)        
      current_row.append(formatted_cell)
    
    if is_first_row:
      colspan_size = len(current_row)
    
    filtered_row = list(set(current_row))
    filtered_row_len = len(filtered_row)

    joined_row = "".join(filtered_row)

    if colspan_size != 0 and filtered_row_len != colspan_size:
      current_colspan_size = colspan_size // filtered_row_len
      joined_row = joined_row.replace("<td>", f"<td colspan='{current_colspan_size}' style='border: 2px solid #006fbf; border-radius: 5px;padding:5px;'>")
    else:
      joined_row = joined_row.replace("<td>", "<td style='border: 2px solid #006fbf;border-radius: 5px;padding:5px;'>")

    table_html += f"<tr>{joined_row}</tr>"
    
    current_row = []
    is_first_row = False
  
  return f"<table style='text-align:center;'>{table_html}</table>"
