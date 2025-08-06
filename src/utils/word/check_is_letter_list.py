from docx.text.paragraph import Paragraph
from docx.oxml.numbering import CT_NumPr, CT_Numbering, CT_Num
from docx.oxml.shared import CT_DecimalNumber

def get_numbered_paragraph(paragraph: Paragraph) -> CT_NumPr:
  xml_paragraph = paragraph._p
  numbered_paragraph = xml_paragraph.find('.//w:numPr', paragraph._element.nsmap)
  return numbered_paragraph

def get_paragraph_id(paragraph: Paragraph, numbered_paragraph: CT_NumPr) -> CT_DecimalNumber:    
  paragraph_id = numbered_paragraph.find('.//w:numId', paragraph._element.nsmap)
  return paragraph_id

def get_paragraph_level(paragraph: Paragraph, numbered_paragraph: CT_NumPr) -> CT_DecimalNumber:    
  paragraph_level = numbered_paragraph.find('.//w:ilvl', paragraph._element.nsmap)
  return paragraph_level

def get_list_id(model_id: CT_DecimalNumber) -> str:
  list_id = model_id.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
  return list_id

def get_list_level(paragraph_level: CT_DecimalNumber) -> str:
   list_level = paragraph_level.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if paragraph_level is not None else '0'
   return list_level

def get_list_model(paragraph: Paragraph) -> CT_Numbering:
   list_model =  paragraph.part.numbering_part.numbering_definitions._numbering
   return list_model

def get_num_node(paragraph: Paragraph, list_id=str, list_model=CT_Numbering):
  num_node = list_model.find(f'.//w:num[@w:numId="{list_id}"]', paragraph._element.nsmap)
  return num_node

def get_list_model_id(num_node: CT_Num, paragraph: Paragraph) -> CT_DecimalNumber:
   list_model_id = num_node.find('.//w:abstractNumId', paragraph._element.nsmap)
   return list_model_id

def get_node_format(node_level, paragraph: Paragraph):
   node_format = node_level.find('.//w:numFmt', paragraph._element.nsmap)
   return node_format

def check_is_letter_list(paragraph: Paragraph) -> bool:      
  numbered_paragraph = get_numbered_paragraph(paragraph)

  if numbered_paragraph is None:
      return False
  
  paragraph_id = get_paragraph_id(paragraph, numbered_paragraph)
  
  if paragraph_id is None:
      return False
  
  paragraph_level = get_paragraph_level(paragraph, numbered_paragraph)  
  
  list_level = get_list_level(paragraph_level)
  list_model = get_list_model(paragraph)
  list_id = get_list_id(paragraph_id)  

  num_node = get_num_node(paragraph=paragraph, list_id=list_id, list_model=list_model)
  if num_node is None:
      return False
  
  list_model_id = get_list_model_id(num_node, paragraph)  
  if list_model_id is None:
      return False

  abstractNumId = get_list_id(list_model_id)
  abstract_node = list_model.find(f'.//w:abstractNum[@w:abstractNumId="{abstractNumId}"]', paragraph._element.nsmap)
  if abstract_node is None:
      return False

  node_level = abstract_node.find(f'.//w:lvl[@w:ilvl="{list_level}"]', paragraph._element.nsmap)
  if node_level is None:
      return False

  node_format = get_node_format(node_level, paragraph)
  if node_format is None:
      return False

  numFmt_val = node_format.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
  
  return numFmt_val in ('lowerLetter', 'upperLetter')