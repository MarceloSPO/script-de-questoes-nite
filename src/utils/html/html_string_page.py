from pathlib import Path

def _load_html_template():

  current_dir = Path(__file__).parent.parent.parent
  template_path = current_dir / "templates" / "index.html"

  with open(template_path, "r", encoding="utf-8") as file:
    return file.read()

html_string_page = _load_html_template()
