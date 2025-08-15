import re

def get_ppd_question_id(text: str):    
  id_regex_pattern = re.compile(
    r"(?<!\w)"
    r"PPD_[A-Z]{2}_\d{2}_"
    r"[A-Za-z0-9_]+_"
    r"[A-Z]\d_"
    r"(?:\d{4}[-_]\d)_"
    r"Q\d{2}"
    r"(?!\w)"
)

  result = re.findall(id_regex_pattern, text)
  if result:
      return result[0]
  return None