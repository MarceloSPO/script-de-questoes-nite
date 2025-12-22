from typing import Any

from questions_types.question import MultipleChoiceQuestion
import utils.csv.platform_a.generate_question_attributes as questions_helper

def generate_platform_a_csv(csv_writer: Any, questions: list[MultipleChoiceQuestion], discipline_code: str="", grade_code: str=""):
  header = questions_helper.generate_question_header(questions)

  csv_writer.writerow(header)

  for question in questions:
    question_row = questions_helper.generate_question_line(question, discipline_code=discipline_code, grade_code=grade_code)

    csv_writer.writerow(question_row)