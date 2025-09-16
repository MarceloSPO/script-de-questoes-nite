import re

def get_question_id(text: str):
  id_regex_pattern = r"^[a-zA-Z0-9]+(?:[-_][a-zA-Z0-9]+)*$"

  
  result = re.findall(id_regex_pattern, text)
  if result:
    return result[0]
  return None
