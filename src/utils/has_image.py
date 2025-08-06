from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

def has_image(paragraph: Paragraph):
  for run in paragraph.runs:
      if run._element.find(qn('w:drawing')) is not None or run._element.find(qn('w:pict')) is not None:
          return True
  return False