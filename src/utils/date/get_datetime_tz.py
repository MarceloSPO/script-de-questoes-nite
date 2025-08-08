from datetime import datetime
from zoneinfo import ZoneInfo

def get_date_time_tz() -> str:
  now = datetime.now()
  timezone_info = str(now.tzinfo)
  

  selected_timezone = "America/Sao_Paulo"

  if timezone_info != selected_timezone:
    now = now.replace(tzinfo=ZoneInfo(selected_timezone))

  formatted_time = now.strftime(r"%d_%m_%Y")
  milliseconds = now.microsecond // 1000
    
  date_time = f"{str(formatted_time).split(" ")[0]}_{milliseconds}"
  return date_time