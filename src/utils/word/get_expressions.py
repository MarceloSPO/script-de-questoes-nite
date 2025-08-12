from lxml import etree
from docx.text.run import Run
from docx.table import _Cell

def get_text_expressions(textual_element):
  xml = ""

  if isinstance(textual_element, _Cell):    
    xml = textual_element._tc.xml
  elif hasattr(textual_element, '_p'):        
    xml = textual_element._p.xml    
  elif isinstance(textual_element, Run):
    xml = textual_element._r.xml
  else:          
    return str(textual_element)
  tree = etree.fromstring(xml)
  
  # print("xml", xml)
  texts = tree.xpath('.//w:t/text() | .//m:t/text() | .//m:paren/text() | .//m:f//text()', namespaces={
      'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
  })
  
  return "".join(texts).strip()
