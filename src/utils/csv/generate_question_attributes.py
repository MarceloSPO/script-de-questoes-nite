

def generate_question_header(question_type: str):
  return ["NewQuestion", question_type, "", ""]

def generate_question_id(id: str):
  return ["ID", id, "", ""]

def generate_question_text(question_text: str):
  return ["QuestionText", question_text, "", ""]

def generate_question_points(points: int):
  return ["Points", points, "",  ""]

def generate_question_option(option_text: str, points: int, feedback: str = ""):
  return ["Option", points, option_text, "", feedback]

def generate_empty_row():
  return ["", "", "", "", ""]