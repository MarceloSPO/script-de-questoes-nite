from docx.text.paragraph import Paragraph

def has_image(paragraph: Paragraph):
    p = paragraph._element    
    if p.xpath('.//*[local-name()="drawing"]'):
        return True    
    if p.xpath('.//*[local-name()="pict"]//*[local-name()="imagedata"]'):
        return True
    if p.xpath('.//*[local-name()="object"]//*[local-name()="imagedata"]'):
        return True
    return False