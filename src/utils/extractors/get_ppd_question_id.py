import re

def get_ppd_question_id(text: str):    
  id_regex_pattern = re.compile(
   r"(?<!\w)PPD_[A-Z]{2}_\d{2,4}_(?:.+?_)?P\d{1,2}_(?:(?:\d{4}[-_]\d)_)?Q\d{1,2}(?!\w)"
)

  result = re.findall(id_regex_pattern, text)
  if result:
      return result[0]
  return None