import copy
from questions_types.question import MultipleChoiceQuestion, QuestionError

from utils.error_messages import error_messages
from utils.generate_question_error import generate_question_error

def add_question_error(question_error: MultipleChoiceQuestion, error_type: str, errors: list[QuestionError]):
  copied_question = copy.deepcopy(question_error)        
  error_message = error_messages[error_type]
  
  question_error = generate_question_error(copied_question, error_message)      
  errors.append(question_error)  