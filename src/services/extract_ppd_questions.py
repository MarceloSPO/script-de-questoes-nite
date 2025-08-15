from docx import Document

from docx.table import _Row

from questions_types.question import MultipleChoiceQuestion, QuestionError

from utils.extractors.question_getters import get_empty_question, get_empty_option
from utils.extractors.get_ppd_question_id import get_ppd_question_id
from utils.extractors.add_question_error import add_question_error

from utils.word.get_list_prefix import prefix_list_items_sequenced
from utils.has_image import has_image
from utils.word.get_styled_paragraph_str import get_styled_paragraph_str

def check_is_ppd_id(text: str):
  return True if "Identificação da questão" in text and bool(get_ppd_question_id(text)) else False

def get_row_text(row: _Row):
  row_text = [cell.text for cell in row.cells]
  row_text = "".join(list(dict.fromkeys(row_text)))

  return row_text

def extract_ppd_questions(file_path: str, are_questions_random: bool = False):
  doc = Document(file_path)
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
        else:
          add_question_error(question_error=question, error_type="question_without_id", errors=question_errors, extra_text=f"({index + 1}º questão)")
      elif row_index == 1 or row_index == 2:
        current_row = []

        for cell in row.cells:
          cell_text = ""
          question_text_prefix_counter = {}

          for index, paragraph in enumerate(cell.paragraphs):
            if paragraph.runs:
              paragraph.runs[0].text = paragraph.runs[0].text.replace("Texto-base:", "").replace("Enunciado:", "")               
            
            if question_has_image:     
              add_question_error(
                question_error=question,
                error_type="question_with_image",
                errors=question_errors
              )
              
            prefix = prefix_list_items_sequenced(paragraph, question_text_prefix_counter)            
            if prefix:
              prefix = f"{prefix} "
            
            formatted_paragraph = get_styled_paragraph_str(paragraph, prefix)
            cell_text += formatted_paragraph
          current_row.append(cell_text)
        filtered_row = list(dict.fromkeys(current_row))
        joined_row = "".join(filtered_row)
        question["question_text"] += joined_row      

  
  print("QUESTIon", question)
        
  return { "questions": [], "errors": [] }