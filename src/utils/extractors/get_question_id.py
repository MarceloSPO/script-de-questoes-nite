import re

def get_question_id(text: str):
  id_regex_pattern = r"\b\w{4}_\w{6}_\w{6}_\w{6}_\w{4}\b"
  result = re.findall(id_regex_pattern, text)

  if result:
    return result[0]
  return None
