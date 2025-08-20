import csv

from questions_types.question import MultipleChoiceQuestion

import utils.csv.generate_question_attributes as questions_helper

def generate_csv(questions: list[MultipleChoiceQuestion], csv_filename: str):   
  with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)

    for question in questions:    
      question_header = questions_helper.generate_question_header("MC")
      question_id = questions_helper.generate_question_id(question["id"])
      question_title = questions_helper.generate_question_title(question["title"])
      question_text = questions_helper.generate_question_text(question["question_text"], format_html=True)
      question_points = questions_helper.generate_question_points(question["points"])
      question_feedback = questions_helper.generate_question_feedback(question["feedback"])

      writer.writerow(question_header)
      writer.writerow(question_id)
      writer.writerow(question_title)
      writer.writerow(question_text)
      writer.writerow(question_points)

      for option in question["options"]:
        question_option = questions_helper.generate_question_option(option_text=option["text"], points=option["answer_value"], feedback=option["feedback"], format_html=True)

        writer.writerow(question_option)

      writer.writerow(question_feedback)
      
      empty_row = questions_helper.generate_empty_row()
      writer.writerow(empty_row)
      writer.writerow(empty_row)
      