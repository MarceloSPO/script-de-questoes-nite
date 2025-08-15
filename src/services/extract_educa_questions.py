from docx import Document
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_COLOR_INDEX

import re

import copy

from typing import TypedDict


from utils.word.get_styled_paragraph_str import get_styled_paragraph_str
from utils.word.check_is_letter_list import check_is_letter_list
from utils.word.get_list_prefix import prefix_list_items_sequenced
from utils.word.is_paragraph import is_paragraph
from utils.word.is_table import is_table
from utils.word.read_table import read_table
from utils.has_image import has_image
from utils.error_messages import error_messages
from utils.generate_question_error import generate_question_error

from questions_types.question import MultipleChoiceQuestion, QuestionError

class Extract_Question_Props_Return(TypedDict):
  questions: list[MultipleChoiceQuestion]
  errors: list[QuestionError]

def get_question_id(text: str):
  id_regex_pattern = r"\b\w{4}_\w{6}_\w{6}_\w{6}_\w{4}\b"
  result = re.findall(id_regex_pattern, text)

  if result:
    return result[0]
  return None


def check_is_question_filled(question: MultipleChoiceQuestion):
  are_filled = question["id"] and len(question["options"]) and question["question_text"]

  return bool(are_filled)

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

def get_empty_option() -> MultipleChoiceQuestion:
  return {
    "answer_value": 0,
    "feedback": None,
    "text": ""
  }

def add_question_error(question_error: MultipleChoiceQuestion, error_type: str, errors: list[QuestionError]):
  copied_question = copy.deepcopy(question_error)        
  error_message = error_messages[error_type]
  
  question_error = generate_question_error(copied_question, error_message)      
  errors.append(question_error)             

def extract_educa_questions(file_path: str, are_questions_random: bool = True) -> Extract_Question_Props_Return:
  doc = Document(file_path)
  questions:list[MultipleChoiceQuestion] = []
  question = get_empty_question()
  current_option = get_empty_option()

  question_errors:list[QuestionError] = []

  option_prefix_counter = {}
  question_text_prefix_counter = {}

  question_has_image = False
  option_has_image = False  

  for index, element in enumerate(doc.element.body):    
    if is_paragraph(element):      
      paragraph = Paragraph(element, doc)
      text_paragraph = paragraph.text.strip()
      is_paragraph_empty = len(text_paragraph) == 0
      is_letter_list = check_is_letter_list(paragraph)      

      if(is_paragraph_empty):
        if has_image(paragraph):      
          add_question_error(question_error=question, error_type="question_with_image", errors=question_errors)
        continue
      
      question_id = get_question_id(text_paragraph)      
          
      if is_letter_list:
        for run in paragraph.runs:
          if run.font.highlight_color == WD_COLOR_INDEX.YELLOW:
            current_option["answer_value"] = 100
            break

        prefix = prefix_list_items_sequenced(paragraph, option_prefix_counter)        
        option_has_image = has_image(paragraph)      

        if option_has_image:          
          add_question_error(
            question_error=question, 
            error_type="option_with_image", 
            errors=question_errors)
                  
          option_has_image = False   

        if prefix and not are_questions_random:
          prefix = f"{prefix} "
        else:
          prefix = None

        current_option["text"] += get_styled_paragraph_str(paragraph, prefix)

        
        question["options"].append(current_option)        
        current_option = get_empty_option()
      elif question_id:      
        is_question_filled = check_is_question_filled(question)
        is_first_item = index == 0      

        if is_question_filled:        
          questions.append(question)             
          question = get_empty_question()  
        elif not is_first_item:
          add_question_error(
            question_error=question,
            error_type="question_without_options",
            errors=question_errors
          )                               


        question["id"] = question_id
        question["title"] = question_id
      else:
        question_has_image = has_image(paragraph)                
        prefix = prefix_list_items_sequenced(paragraph, question_text_prefix_counter)        
        if question_has_image:          
          add_question_error(
            question_error=question,
            error_type="question_with_image",
            errors=question_errors
          )
          

        if prefix:
          prefix = f"{prefix} "        

        question["question_text"] += get_styled_paragraph_str(paragraph, prefix)
    elif is_table(element):      
      table_html = read_table(element, doc)
      question["question_text"] += f"\n\n{table_html}\n\n"

          

  if check_is_question_filled(question):
    questions.append(question)
  else:
    add_question_error(
      question_error=question,
      error_type="question_without_options",
      errors=question_errors
    )
  
  return { "questions": questions, "errors": question_errors }