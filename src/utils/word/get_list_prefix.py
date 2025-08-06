from docx.text.paragraph import Paragraph

def to_roman(n):
    val_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'),  (90, 'XC'), (50, 'L'),  (40, 'XL'),
        (10, 'X'),   (9, 'IX'),  (5, 'V'),   (4, 'IV'), (1, 'I')
    ]
    result = ''
    for arabic, roman in val_map:
        while n >= arabic:
            result += roman
            n -= arabic
    return result

def to_letter(n, upper=True):
    result = ''
    while n > 0:
        n -= 1
        result = chr((n % 26) + (65 if upper else 97)) + result
        n //= 26
    return result

formatters = {
    'decimal':      lambda i: f"{i}.",
    'lowerLetter':  lambda i: f"{to_letter(i, upper=False)})",
    'upperLetter':  lambda i: f"{to_letter(i, upper=True)})",
    'lowerRoman':   lambda i: f"{to_roman(i).lower()})",
    'upperRoman':   lambda i: f"{to_roman(i)})",
    'bullet':       lambda i: "•",
}

def prefix_list_items_sequenced(paragraph: Paragraph, counters: dict):
    p = paragraph._p
    nsmap = paragraph._element.nsmap

    numPr = p.find('.//w:numPr', nsmap)
    if numPr is None:
        return None 

    numId_el = numPr.find('.//w:numId', nsmap)
    ilvl_el = numPr.find('.//w:ilvl', nsmap)

    if numId_el is None:
        return None

    numId = numId_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
    ilvl = ilvl_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if ilvl_el is not None else '0'
    
    key = (numId, ilvl)
    counters[key] = counters.get(key, 0) + 1
    count = counters[key]

    numbering = paragraph.part.numbering_part.numbering_definitions._numbering
    num_node = numbering.find(f'.//w:num[@w:numId="{numId}"]', nsmap)
    if num_node is None:
        return None

    abstractNumId_el = num_node.find('.//w:abstractNumId', nsmap)
    if abstractNumId_el is None:
        return None

    abstractNumId = abstractNumId_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
    abstract_node = numbering.find(f'.//w:abstractNum[@w:abstractNumId="{abstractNumId}"]', nsmap)
    if abstract_node is None:
        return None

    lvl_node = abstract_node.find(f'.//w:lvl[@w:ilvl="{ilvl}"]', nsmap)
    if lvl_node is None:
        return None

    numFmt_node = lvl_node.find('.//w:numFmt', nsmap)
    if numFmt_node is None:
        return None

    numFmt_val = numFmt_node.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')

    formatter = formatters.get(numFmt_val)
    if formatter:
        return formatter(count)
    return None
