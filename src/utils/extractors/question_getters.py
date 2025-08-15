from questions_types.question import MultipleChoiceQuestion, MultipleChoiceOption

def get_empty_question() -> MultipleChoiceQuestion:
  return {
    "id": None,
    "difficulty": None,
    "image": None,
    "options": [],
    "points": None,
    "question_text": "",
    "title": None
  }

def get_empty_option() -> MultipleChoiceOption:
  return {
    "answer_value": 0,
    "feedback": None,
    "text": ""
  }