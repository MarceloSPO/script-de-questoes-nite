import re

def get_ppd_question_id(text: str):    
  id_regex_pattern = re.compile(
   r"\b\w{1,4}_\w{1,6}_\w{1,6}_\w{1,6}_\w{1,4}\b"
)

  result = re.findall(id_regex_pattern, text)
  if result:
      return result[0]
  return None