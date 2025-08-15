from typing import TypedDict

from questions_types.question import MultipleChoiceQuestion, QuestionError

class ExtractQuestionPropsReturn(TypedDict):
  questions: list[MultipleChoiceQuestion]
  errors: list[QuestionError]