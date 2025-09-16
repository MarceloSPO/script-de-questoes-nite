from docx.text.paragraph import Paragraph
from utils.word.namespaces import NAMESPACES
from utils.word.font_size_map import font_size_map

def get_paragraph_font_size(paragraph: Paragraph):
  pPr = paragraph._element.pPr
  
  size = font_size_map[12.0]

  if not pPr:
    return size
  sz = pPr.find(".//w:sz", NAMESPACES)
          
  if sz is not None:
    size_val = int(sz.get(f"{{{NAMESPACES['w']}}}val")) / 2
    if size_val in font_size_map:
      size = font_size_map[size_val]

  return size