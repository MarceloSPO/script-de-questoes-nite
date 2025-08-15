import os

from services.extract_questions import extract_questions
from services.generate_csv import generate_csv

from utils.csv.generate_csv_filename import generate_csv_filename

def convertor(filename: str):  
  csv_filename = generate_csv_filename(filename)

  base_path = os.path.dirname(os.path.abspath(__file__))

  file_path = os.path.join(base_path, "assets", "word", filename)  

  extracted = extract_questions(file_path, are_questions_random=False)
  questions = extracted["questions"]
  errors = extracted["errors"]

  for error in errors:
    print(f"QUESTÃO FALHOU: {error["question"]["id"]}")
    print(f"MOTIVO: {error['message']}\n\n")  

  generate_csv(questions, csv_filename)

  return { "errors": errors, "had_error": True if len(errors) > 0 else False }

convertor(filename="modelo-de-questao-educa.docx")