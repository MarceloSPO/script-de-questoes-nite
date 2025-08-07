from utils.date.get_date_tz import get_date_tz
from utils.format_filename import format_filename

def generate_csv_filename(filename: str) -> str:
  date = get_date_tz()
  
  new_filename = format_filename(filename)
  new_filename = new_filename.split(".")[0]

  new_filename = f"{new_filename}_{date}.csv"

  return new_filename