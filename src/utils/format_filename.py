def format_filename(filename: str) -> str:
  
  return filename.lower().strip().replace("- ", "", -1).replace(" ", "_", -1)