import csv
import io

from enums.platform_types import PlatformType
from questions_types.question import MultipleChoiceQuestion

from services.generate_ava_csv import generate_ava_csv
from services.generate_platform_a_csv import generate_platform_a_csv
from utils.csv.get_delimiter import get_delimiter


def generate_csv_from_buffer(questions: list[MultipleChoiceQuestion], platform_type: PlatformType):     
  buffer = io.StringIO()
  delimiter = get_delimiter(platform_type)
  writer = csv.writer(buffer, delimiter=delimiter)

  if platform_type == PlatformType.AVA:
    generate_ava_csv(writer, questions=questions)
  elif platform_type == PlatformType.PLATAFORMA_A:
    generate_platform_a_csv(writer, questions=questions)
  buffer.seek(0)  
  return buffer
    