import os

from enum import Enum

from services.extract_educa_questions import extract_educa_questions
from services.generate_csv import generate_csv

from utils.csv.generate_csv_filename import generate_csv_filename

class QuestionsType(Enum):
  EDUCA="educa"
  PPD="ppd"

def convertor(filename: str, type: QuestionsType):  

  base_path = os.path.dirname(os.path.abspath(__file__))  

  file_path = os.path.join(base_path, "assets", "word", filename)

  questions = []
  errors = []

  if type == QuestionsType.EDUCA:
    extracted = extract_educa_questions(file_path, are_questions_random=False)
    questions = extracted["questions"]
    errors = extracted["errors"]
  elif type == QuestionsType.PPD:
    pass
  else:
    raise Exception("O tipo da questão pode apenas ser PPD ou EDUCA!")
  
  for error in errors:
    print(f"QUESTÃO FALHOU: {error["question"]["id"]}")
    print(f"MOTIVO: {error['message']}\n\n")  

  csv_filename = generate_csv_filename(filename)
  generate_csv(questions, csv_filename)  

  return { "errors": errors, "had_error": True if len(errors) > 0 else False }

convertor(filename="modelo-de-questao-educa.docx", type=QuestionsType.EDUCA)