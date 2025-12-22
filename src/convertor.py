from io import BytesIO
import webview
from webview import Window
from enum import Enum

from services.extract_educa_questions import extract_educa_questions
from services.extract_ppd_questions import extract_ppd_questions
from services.generate_csv_from_path import generate_csv_from_path
from services.generate_csv_from_buffer import generate_csv_from_buffer

from utils.csv.generate_csv_filename import generate_csv_filename

class QuestionsType(Enum):
  EDUCA="educa"
  PPD="ppd"

class PlatformType(Enum):
  AVA="ambiente-de-aprendizagem-virtual"
  PLATAFORMA_A = "plataforma-a"

def convertor(
  filename: str, 
  file_stream: BytesIO, 
  are_questions_random: bool, 
  type: QuestionsType, 
  platform_type: PlatformType, 
  window: Window=None):    
  questions = []
  errors = []

  if type == QuestionsType.EDUCA:
    extracted = extract_educa_questions(file_stream, are_questions_random=are_questions_random)
    questions = extracted["questions"]
    errors = extracted["errors"]    
  elif type == QuestionsType.PPD:    
    extracted = extract_ppd_questions(file_stream, are_questions_random=are_questions_random)
    questions = extracted["questions"]
    errors = extracted["errors"]
  else:
    raise Exception("O tipo da questão pode apenas ser PPD ou EDUCA!")

  csv_filename = generate_csv_filename(filename)
  csv_buffer = None

  if window:
    file_path = (window.create_file_dialog(
        webview.FileDialog.SAVE,
        save_filename=csv_filename,
        file_types=("CSV files (*.csv)", "All files (*.*)")
    ))[0]    
    
    if file_path:
        generate_csv_from_path(questions, file_path)
  else:
    csv_buffer = generate_csv_from_buffer(questions)  

  return { "errors": errors, "had_error": True if len(errors) > 0 else False, "csv": { "buffer": csv_buffer, "filename": csv_filename } }