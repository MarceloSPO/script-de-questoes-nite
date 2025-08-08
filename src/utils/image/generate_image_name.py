from utils.date.get_datetime_tz import get_date_time_tz

def generate_image_name(filename: str, extension: str):
  splitted_filename = filename.split(".")[0].strip()
  date_time = get_date_time_tz()

  image_name = f"{splitted_filename}_{date_time}.{extension}".lower()

  return image_name
