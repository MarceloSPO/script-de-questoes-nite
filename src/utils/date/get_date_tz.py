from datetime import datetime
from zoneinfo import ZoneInfo

def get_date_tz() -> str:
  now = datetime.now()
  timezone_info = str(now.tzinfo)

  selected_timezone = "America/Sao_Paulo"

  if timezone_info != selected_timezone:
    now = now.replace(tzinfo=ZoneInfo(selected_timezone))

  now = now.strftime(r"%d_%m_%Y")
  now = str(now).split(" ")[0]
  return now