from typing import TypedDict

class MultipleChoiceOption(TypedDict):
  answer_value: int
  text: str
  feedback: str

class MultipleChoiceQuestion(TypedDict):
  id: str
  title: str
  question_text: str
  points: int
  difficulty: int
  image: str
  options: list[MultipleChoiceOption]


