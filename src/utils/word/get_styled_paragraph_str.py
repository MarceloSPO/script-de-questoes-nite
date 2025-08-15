from docx.text.paragraph import Paragraph

from utils.word.get_expressions import get_text_with_math_and_html
from utils.word.get_paragraph_css_alignment import get_paragraph_css_alignment
from utils.word.get_paragraph_font_size import get_paragraph_font_size

def get_styled_paragraph_str(paragraph: Paragraph, prefix: str | None=""):
  paragraph_in_html = get_text_with_math_and_html(paragraph)
  question_text = paragraph_in_html.strip()

  size = get_paragraph_font_size(paragraph)
  css_alignment = get_paragraph_css_alignment(paragraph)          
  
  styled_paragraph_str  = f"<p style='font-size:{size};{css_alignment}'>{prefix if prefix else ""}{question_text}</p>"
  
  return styled_paragraph_str