from lxml import etree
from docx.table import _Cell
from docx.text.run import Run
from lxml.etree import _Element

def get_math_expression(element: _Element, ns):
	math_texts = element.xpath('.//m:t/text() | .//m:paren/text() | .//m:f//text()', namespaces=ns)					
	math_exp = "".join(math_texts).strip()
	return math_exp

def get_formatting_expression(child, ns):
	texts = child.xpath('.//w:t/text()', namespaces=ns)
	text = "".join(texts)
	if not text:
		return

	rPr = child.find('w:rPr', namespaces=ns)
	if rPr is not None:
		if rPr.find('w:b', namespaces=ns) is not None:
			text = f"<b>{text}</b>"
		if rPr.find('w:i', namespaces=ns) is not None:
			text = f"<i>{text}</i>"
		if rPr.find('w:u', namespaces=ns) is not None:
			text = f"<u>{text}</u>"
		if rPr.find('w:strike', namespaces=ns) is not None:
			text = f"<s>{text}</s>"
	return text

def get_text_with_math_and_html(textual_element):

	if isinstance(textual_element, _Cell):
		xml = textual_element._tc.xml
	elif hasattr(textual_element, '_p'):
		xml = textual_element._p.xml
	elif isinstance(textual_element, Run):
		xml = textual_element._r.xml
	else:
		return str(textual_element)

	tree = etree.fromstring(xml)	
	ns = {
		'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
		'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
	}

	parts = []	
	if isinstance(textual_element, _Cell):
		paragraphs = tree.xpath('.//w:p', namespaces=ns)		
		for p in paragraphs:            			
			for child in p:
				tag = etree.QName(child.tag).localname				
				ns_uri = etree.QName(child.tag).namespace

				if ns_uri == ns['w'] and tag == 'r':
					text = get_formatting_expression(child, ns)

					if not text:					
						continue

					parts.append(text)

				elif ns_uri == ns['m'] and tag in ('oMath', 'oMathPara'):					
					math_exp = get_math_expression(child, ns)					
					parts.append(math_exp)			
			return "".join(parts).strip()

	else:		
		for child in tree:
			tag = etree.QName(child.tag).localname
			ns_uri = etree.QName(child.tag).namespace

			if ns_uri == ns['w'] and tag == 'r':
				text = get_formatting_expression(child, ns)

				if not text:					
					continue

				parts.append(text)

			elif ns_uri == ns['m'] and tag in ('oMath', 'oMathPara'):					
				math_exp = get_math_expression(child, ns)
				parts.append(math_exp)

		return "".join(parts).strip()
