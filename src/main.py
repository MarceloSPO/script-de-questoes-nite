import sys, os, webview
import base64
from io import BytesIO
from convertor import QuestionsType

from convertor import convertor

from utils.html_page import html_page

# window = None

def resource_path(relative_path):    
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Api:
    def __init__(self, window):
      self.window = window
    def process_form(self, filename, file_base64, option, are_questions_random):
      file_bytes = base64.b64decode(file_base64)
      file_stream = BytesIO(file_bytes)      
      type = QuestionsType.EDUCA if option == "EDUCA" else QuestionsType.PPD                  
      res = convertor(filename, file_stream, are_questions_random, type, self.window)

      return res

def main():        
    api = Api(None)  # cria com None e depois setamos
    window = webview.create_window("Script de questões | NITE", html=html_page, js_api=api)
    api.window = window  # injeta o window dentro do api
    webview.start()

if __name__ == "__main__":
    main()
