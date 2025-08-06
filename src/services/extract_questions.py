from docx import Document
from docx.enum.text import WD_COLOR_INDEX

import re


from typing import TypedDict

from utils.word.check_is_letter_list import check_is_letter_list
from utils.word.get_list_prefix import prefix_list_items_sequenced
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




def get_question_id(text: str):
  id_regex_pattern = r"\b\w{4}_\w{6}_\w{6}_\w{6}_\w{4}\b"
  result = re.findall(id_regex_pattern, text)

  if result:
    return result[0]
  return None


def check_is_question_filled(question: MultipleChoiceQuestion):
  are_filled = question["id"] and len(question["options"]) and question["question_text"]

  return are_filled

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


def extract_questions(file_path: str):
  doc = Document(file_path)
  questions:list[MultipleChoiceQuestion] = []
  question = get_empty_question()
  current_option = get_empty_option()
  
  option_prefix_counter = {}
  question_text_prefix_counter = {}

  for paragraph in doc.paragraphs:    
    text_paragraph = paragraph.text.strip()
    is_paragraph_empty = len(text_paragraph) == 0
    is_letter_list = check_is_letter_list(paragraph)


    if(is_paragraph_empty):
      continue
     
    question_id = get_question_id(text_paragraph)      
        
    if is_letter_list:                
      for run in paragraph.runs:
        if run.font.highlight_color == WD_COLOR_INDEX.YELLOW:
          current_option["answer_value"] = 100      
          break

      prefix = prefix_list_items_sequenced(paragraph, option_prefix_counter)
      option_text = text_paragraph

      if prefix:
        option_text = f"\n{prefix} {option_text}\n"

      current_option["text"] += option_text

      
      question["options"].append(current_option)        
      current_option = get_empty_option()
    elif question_id:      
      is_question_filled = check_is_question_filled(question)
            
      if is_question_filled:
        questions.append(question)        
        question = get_empty_question()


      question["id"] = question_id      
    else:
      prefix = prefix_list_items_sequenced(paragraph, question_text_prefix_counter)
      question_text = text_paragraph

      if prefix:
        question_text = f"\n{prefix} {text_paragraph}\n"
      
      question["question_text"] += question_text

  if check_is_question_filled(question):
    questions.append(question)
  
  return questions