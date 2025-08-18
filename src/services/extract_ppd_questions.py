from io import BytesIO
from docx import Document

from docx.text.paragraph import Paragraph
from docx.table import _Row
from docx.enum.text import WD_COLOR_INDEX

from questions_types.question import MultipleChoiceQuestion, QuestionError

from utils.extractors.question_getters import get_empty_question, get_empty_option
from utils.extractors.get_ppd_question_id import get_ppd_question_id
from utils.extractors.add_question_error import add_question_error

from utils.word.get_list_prefix import prefix_list_items_sequenced
from utils.has_image import has_image
from utils.word.get_styled_paragraph_str import get_styled_paragraph_str
from utils.word.check_is_letter_list import check_is_letter_list
from utils.word.is_table import is_table
from utils.word.is_paragraph import is_paragraph
from utils.word.read_table import read_table

def check_is_ppd_id(text: str):
  return True if "Identificação da questão" in text and bool(get_ppd_question_id(text)) else False

def get_row_text(row: _Row):
  row_text = [cell.text for cell in row.cells]
  row_text = "".join(list(dict.fromkeys(row_text)))

  return row_text

def handle_format_with_html_and_prefix(paragraph: Paragraph, with_prefix: bool, option_prefix_counter):  
  prefix = prefix_list_items_sequenced(paragraph, option_prefix_counter)            
  if prefix and with_prefix:
    prefix = f"{prefix} "
  else:
    prefix = None
  
  formatted_paragraph = get_styled_paragraph_str(paragraph, prefix)
  return formatted_paragraph

def extract_ppd_questions(file_stream: BytesIO, are_questions_random: bool = False):
  doc = Document(file_stream)
  questions:list[MultipleChoiceQuestion] = []
  question = get_empty_question()
  current_option = get_empty_option()

  question_errors:list[QuestionError] = []

  option_prefix_counter = {}

  question_has_image = False
  option_has_image = False

  for index, table in enumerate(doc.tables[1:]):
    for row_index, row in enumerate(table.rows[1:]):
      if row_index == 0:
        row_text = get_row_text(row)
        is_ppd_id = check_is_ppd_id(row_text)        

        if is_ppd_id:
          ppd_id = get_ppd_question_id(row_text)
          question["id"] = ppd_id
          question["title"] = ppd_id
        else:
          question["id"] = get_ppd_question_id(row_text)
          add_question_error(question_error=question, error_type="question_without_id", errors=question_errors, extra_text=f"({index + 1}º questão)")
      elif row_index == 1 or row_index == 2:
        question_text_prefix_counter = {}
        for cell in list(dict.fromkeys(row.cells)):
          for element in cell._tc.iterchildren():
            if is_paragraph(element):
              paragraph = Paragraph(element, cell)                  
              if paragraph.runs:
                paragraph.runs[0].text = paragraph.runs[0].text.replace("Texto-base:", "").replace("Enunciado:", "")                                      
              if has_image(paragraph):
                add_question_error(
                    question_error=question,
                    error_type="question_with_image",
                    errors=question_errors
                )                                      
              formatted_paragraph = handle_format_with_html_and_prefix(
                paragraph,
                with_prefix=True,
                option_prefix_counter=question_text_prefix_counter
              )
              question["question_text"] += formatted_paragraph
            elif is_table(element):            
              table_html = read_table(element, cell)
              question["question_text"] += f"\n\n{table_html}\n\n"
      elif row_index == 3:
        for cell in list(dict.fromkeys(row.cells)):
          question_text_prefix_counter = {}      
          for paragraph in cell.paragraphs:            
            if paragraph.runs:
                paragraph.runs[0].text = paragraph.runs[0].text.replace("Alternativas:", "")
            
            is_letter_list = check_is_letter_list(paragraph)
    
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
            else:
              question_has_image = has_image(paragraph)
              if question_has_image:     
                add_question_error(
                  question_error=question,
                  error_type="question_with_image",
                  errors=question_errors
                )
              formatted_paragraph = handle_format_with_html_and_prefix(paragraph, with_prefix=True, option_prefix_counter=question_text_prefix_counter)
              question["question_text"] += formatted_paragraph
      elif row_index == 5:
        for cell in list(dict.fromkeys(row.cells)):
          question_text_prefix_counter = {}      
          for paragraph in cell.paragraphs: 
            if paragraph.runs:
              paragraph.runs[0].text = paragraph.runs[0].text.replace("Feedback:", "")

            question_has_image = has_image(paragraph)
            if question_has_image:     
              add_question_error(
                question_error=question,
                error_type="feed_back_with_image",
                errors=question_errors
              )
            formatted_paragraph = handle_format_with_html_and_prefix(paragraph, with_prefix=True, option_prefix_counter=question_text_prefix_counter)
            
            question["feedback"] += formatted_paragraph              
  questions.append(question)
  question = get_empty_question()
                          
  
  return { "questions": questions, "errors": question_errors }