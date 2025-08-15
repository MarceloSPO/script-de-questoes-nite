import os

from enum import Enum

from services.extract_educa_questions import extract_educa_questions
from services.extract_ppd_questions import extract_ppd_questions
from services.generate_csv import generate_csv

from utils.csv.generate_csv_filename import generate_csv_filename

class QuestionsType(Enum):
  EDUCA="educa"
  PPD="ppd"

def convertor(filename: str, are_questions_random: bool, type: QuestionsType):  

  base_path = os.path.dirname(os.path.abspath(__file__))  

  file_path = os.path.join(base_path, "assets", "word", filename)

  questions = []
  errors = []

  if type == QuestionsType.EDUCA:
    extracted = extract_educa_questions(file_path, are_questions_random=are_questions_random)
    questions = extracted["questions"]
    errors = extracted["errors"]
  elif type == QuestionsType.PPD:    
    extracted = extract_ppd_questions(file_path, are_questions_random=are_questions_random)
  else:
    raise Exception("O tipo da questão pode apenas ser PPD ou EDUCA!")
  
  for error in errors:
    print(f"QUESTÃO FALHOU: {error["question"]["id"]}")
    print(f"MOTIVO: {error['message']}\n\n")  

  csv_filename = generate_csv_filename(filename)
  generate_csv(questions, csv_filename)  

  return { "errors": errors, "had_error": True if len(errors) > 0 else False }

convertor(filename="ppd-teste.docx", are_questions_random=True, type=QuestionsType.PPD)