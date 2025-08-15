from docx import Document
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_COLOR_INDEX


from utils.word.get_styled_paragraph_str import get_styled_paragraph_str
from utils.word.check_is_letter_list import check_is_letter_list
from utils.word.get_list_prefix import prefix_list_items_sequenced
from utils.word.is_paragraph import is_paragraph
from utils.word.is_table import is_table
from utils.word.read_table import read_table
from utils.has_image import has_image

from utils.extractors.get_question_id import get_question_id
from utils.extractors.check_is_question_filled import check_is_question_filled
from utils.extractors.question_getters import get_empty_question, get_empty_option
from utils.extractors.add_question_error import add_question_error

from questions_types.question import MultipleChoiceQuestion, QuestionError
from questions_types.extractors import ExtractQuestionPropsReturn

def extract_educa_questions(file_path: str, are_questions_random: bool = True) -> ExtractQuestionPropsReturn:
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

        option_has_image = has_image(paragraph)      

        if option_has_image:          
          add_question_error(
            question_error=question, 
            error_type="option_with_image", 
            errors=question_errors)
                  
          option_has_image = False   

        prefix = prefix_list_items_sequenced(paragraph, option_prefix_counter)        
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
        if question_has_image:          
          add_question_error(
            question_error=question,
            error_type="question_with_image",
            errors=question_errors
          )
          
        prefix = prefix_list_items_sequenced(paragraph, question_text_prefix_counter)        
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