import logging

import os
import zipfile
import shutil

from services.extract_questions import extract_questions
from services.generate_csv import generate_csv


# filename = "Pedagogia - Teste UCB EaD.docx"
filename = "EXEMPLO.docx"
base_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_path, "assets", "word", filename)

destiny = r".\src\destiny"

logging.basicConfig(filename='log.txt',
    filemode='w',
    level=logging.DEBUG,
    encoding="utf-8")

os.makedirs(destiny, exist_ok=True)

with zipfile.ZipFile(file_path, 'r') as docx_zip:
  for filename in docx_zip.namelist():
    if filename.startswith("word/media/"):
      image_name = os.path.basename(filename)
      destiny_path = os.path.join(destiny, image_name)

      with docx_zip.open(filename) as image:
        with open(destiny_path, 'wb') as out_file:
          shutil.copyfileobj(image, out_file)

questions = extract_questions(file_path)

generate_csv(questions)

