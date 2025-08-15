from questions_types.question import MultipleChoiceQuestion

def check_is_question_filled(question: MultipleChoiceQuestion) -> bool:
  are_filled = question["id"] and len(question["options"]) and question["question_text"]

  return bool(are_filled)