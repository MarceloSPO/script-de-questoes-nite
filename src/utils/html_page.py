from dotenv import load_dotenv
import os
from pathlib import Path
import re

from .get_url_flag import get_url_flag
from .pywebview_bridge_text import pywebview_bridge_text, starting_delimiter, ending_delimiter

load_dotenv()

def get_html_page(html_name:str="index.html", executable:bool=False):
  url_flag = get_url_flag() or os.getenv("SERVER_URL")
  base_dir = Path(__file__).resolve().parent.parent
  path = base_dir / "templates" / html_name
  text_to_replace = 'const URL = "http://exemplo.com";'
  
  html_string = ""
  
  with open(path, "r", encoding="utf-8") as f:
    html_string = f.read()

  if executable:
    start_escaped = re.escape(starting_delimiter)
    end_escaped = re.escape(ending_delimiter)
    html_string = re.sub(fr"({start_escaped}).*?({end_escaped})",
    r"\1\n" + pywebview_bridge_text + r"\n\2",
    html_string,
    flags=re.DOTALL)    
  else:
    html_string = html_string.replace(text_to_replace, f'const URL = "{url_flag}"; // Inserted with python 🐍 [html_page.py]')  
  
  return html_string
