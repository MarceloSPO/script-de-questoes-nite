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
  images: list[str]
  options: list[MultipleChoiceOption]

class QuestionError(TypedDict):
  question: list[MultipleChoiceQuestion]
  message: str
