from questions_types.question import MultipleChoiceQuestion, QuestionError

def generate_question_error(question: MultipleChoiceQuestion, message: str) -> QuestionError:
  return { "question": question, "message": message }