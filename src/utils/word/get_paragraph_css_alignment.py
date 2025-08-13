from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH

def get_paragraph_css_alignment(paragraph: Paragraph):
  alignment = paragraph.alignment

  if alignment == WD_ALIGN_PARAGRAPH.LEFT:
    return "text-align:left;"
  elif alignment == WD_ALIGN_PARAGRAPH.RIGHT:
    return "text-align:right;"
  elif alignment == WD_ALIGN_PARAGRAPH.CENTER:
    return "text-align:center;"
  elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
    return "text-align:justify;text-justify:inter-word;"
  elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY_LOW:
    return "text-align:justify;text-justify:distribute;"
  elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY_MED:
    return "text-align:justify;text-justify:distribute;"
  elif alignment == WD_ALIGN_PARAGRAPH.JUSTIFY_HI:
    return "text-align:justify;text-justify:distribute;"
  elif alignment == WD_ALIGN_PARAGRAPH.THAI_JUSTIFY:
    return "text-align:justify;text-justify:distribute;"
  elif alignment == WD_ALIGN_PARAGRAPH.DISTRIBUTE:
    return "text-align:justify;text-justify:distribute;"
  else:
    return "text-align:justify;text-justify:inter-word;"