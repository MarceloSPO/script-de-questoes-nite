import csv

from enums.platform_types import PlatformType
from questions_types.question import MultipleChoiceQuestion

from services.generate_ava_csv import generate_ava_csv
from services.generate_platform_a_csv import generate_platform_a_csv


def generate_csv_from_path(questions: list[MultipleChoiceQuestion], csv_filename: str, platform_type: PlatformType):   
  with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)

    if platform_type == PlatformType.AVA:
      generate_ava_csv(writer, questions=questions)
    elif platform_type == PlatformType.PLATAFORMA_A:
      generate_platform_a_csv(writer, questions=questions)

      