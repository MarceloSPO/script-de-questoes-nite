import os

from docx.text.paragraph import Paragraph
from docx.document import Document
from docx.oxml.ns import qn

from utils.image.generate_image_name import generate_image_name
from utils.word.namespaces import NAMESPACES

def extract_image_from_paragraph(doc_name: str, doc: Document, paragraph: Paragraph, output_dir: str):
  para_xml = paragraph._element
  
  drawings = para_xml.findall(".//w:drawing", namespaces=para_xml.nsmap)
  image_counter = 0

  if drawings:      
    for drawing in drawings:          
      blip = drawing.find(".//a:blip", namespaces=NAMESPACES)      
      if blip is not None:
        embed_rid = blip.get(qn("r:embed"))
        if embed_rid:                  
          image_part = doc.part.related_parts[embed_rid]
          image_bytes = image_part.blob
          image_extension = image_part.content_type.split("/")[-1]          
          image_filename = generate_image_name(filename=doc_name, extension=image_extension)          
          image_path = os.path.join(output_dir, image_filename)
          with open(image_path, "wb") as f:
            f.write(image_bytes)
          
          image_counter += 1