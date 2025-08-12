import os

from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

def read_docx_in_blocks(path):
  file_path = r"C:\Users\allan\NITE\script-de-questoes-nite\src\assets\word\testes-questoes3.docx"
  print("FILE PATH", file_path)
  doc = Document(file_path)
  blocks = []
  current_block = []


  for element in doc.element.body:
    if element.tag.endswith('p'): 
      paragraph = Paragraph(element, doc)
      current_block.append(paragraph.text)

    elif element.tag.endswith('tbl'): 
      table = Table(element, doc)
      
      if current_block:
        blocks.append(current_block)
        current_block = []
    
      table_data = [
        [cell.text for cell in row.cells]
        for row in table.rows
      ]
      blocks.append(table_data)

  if current_block: 
    blocks.append(current_block)

  return blocks


blocks = read_docx_in_blocks("meuarquivo.docx")
for i, block in enumerate(blocks, start=1):
  print(f"--- Bloco {i} ---")
  if isinstance(block[0], list): 
    for row in block:
      print(row)
  else: 
    for para in block:
      print(para)
