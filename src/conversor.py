from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

import os
import zipfile
import shutil

filename = "cinema.docx"
base_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_path, "assets", "word", filename)
print("file_path", file_path)
destiny = r".\src\destiny"

os.makedirs(destiny, exist_ok=True)

with zipfile.ZipFile(file_path, 'r') as docx_zip:
  for filename in docx_zip.namelist():
    if filename.startswith("word/media/"):
      image_name = os.path.basename(filename)
      destiny_path = os.path.join(destiny, image_name)

      with docx_zip.open(filename) as image:
        with open(destiny_path, 'wb') as out_file:
          shutil.copyfileobj(image, out_file)

doc = Document(file_path)

def has_image(paragraph: Paragraph):
  for run in paragraph.runs:
      if run._element.find(qn('w:drawing')) is not None or run._element.find(qn('w:pict')) is not None:
          return True
  return False

def get_table_text(table: Table):
  for row in table.rows:
    for cell in row.cells:
      for paragraph in cell.paragraphs:
        has_image(paragraph)
        print("paragraph", paragraph)        



for table in doc.tables:
  get_table_text(table)

# HOSPEDAR IMAGENS COM pyimgur

