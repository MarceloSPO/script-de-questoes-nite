from typing import Any

from questions_types.question import MultipleChoiceQuestion
import utils.csv.ava.generate_question_attributes as questions_helper


def generate_ava_csv(csv_writer: Any, questions: list[MultipleChoiceQuestion]):
  for question in questions:    
    question_header = questions_helper.generate_question_header("MC")
    question_id = questions_helper.generate_question_id(question["id"])
    question_title = questions_helper.generate_question_title(question["title"])
    question_text = questions_helper.generate_question_text(question["question_text"], format_html=True)
    question_points = questions_helper.generate_question_points(question["points"])
    question_feedback = questions_helper.generate_question_feedback(question["feedback"])

    csv_writer.writerow(question_header)
    csv_writer.writerow(question_id)
    csv_writer.writerow(question_title)
    csv_writer.writerow(question_text)
    csv_writer.writerow(question_points)

    for option in question["options"]:
      question_option = questions_helper.generate_question_option(option_text=option["text"], points=option["answer_value"], feedback=option["feedback"], format_html=True)

      csv_writer.writerow(question_option)

    csv_writer.writerow(question_feedback)
    
    empty_row = questions_helper.generate_empty_row()
    csv_writer.writerow(empty_row)
    csv_writer.writerow(empty_row) 