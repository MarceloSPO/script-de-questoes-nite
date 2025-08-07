from utils.format_with_html import format_with_html

def generate_question_header(question_type: str):
  return ["NewQuestion", question_type, "", ""]

def generate_question_id(id: str):
  return ["ID", id, "", ""]

def generate_question_title(title: str = ""):
  return ["Title", title, "", ""]

def generate_question_text(question_text: str, format_html:bool=False):
  formatted_text = question_text

  if format_html:
    formatted_text = format_with_html(question_text)

  return ["QuestionText", formatted_text, "HTML" if format_html else "", ""]

def generate_question_points(points: int):
  return ["Points", points, "",  ""]

def generate_question_option(option_text: str, points: int, feedback: str = ""):
  return ["Option", points, option_text, "", feedback]

def generate_empty_row():
  return ["", "", "", "", ""]