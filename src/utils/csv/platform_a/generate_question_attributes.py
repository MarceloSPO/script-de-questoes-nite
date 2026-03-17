

from questions_types.question import MultipleChoiceOption, MultipleChoiceQuestion

def generate_question_header(questions: list[MultipleChoiceQuestion]):
  header = ["titulo", "texto_questao", "tipo"]

  first_question = questions[0]
  options_amount = len(first_question["options"])
  
  for question_number in range(options_amount):
    header.append(f"alternativa_{question_number + 1}")
  
  header_ending = [
    "alternativa_Correta", 
    "feedback", 
    "padrao_resposta", 
    "cpf_elaborador", 
    "codigo_disciplina", 
    "codigo_grade",
    "quantidade_linhas_discursiva,,,,,,,,,,,,,,,,,,,,,,,,"
    ]

  header_final = header + header_ending  
  return header_final

def generate_question_line(question: MultipleChoiceQuestion, discipline_code: str="", grade_code: str=""):
  title = question["title"]
  question_text = question["question_text"]
  question_type = "Objetiva"

  row_content = [title, question_text, question_type]
  correct_answer = -1

  for index, option in enumerate[MultipleChoiceOption](question["options"]):
    is_correct_option = option["answer_value"] == 100

    if is_correct_option:
      correct_answer = index + 1

    row_content.append(option["text"])

  ending_row_content = [correct_answer, question["feedback"], "", "", discipline_code, grade_code, ""]

  row_final = row_content + ending_row_content

  return row_final


