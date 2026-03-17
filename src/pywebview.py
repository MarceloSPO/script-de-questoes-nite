import webview
import base64
from io import BytesIO
from enums.platform_types import PlatformType, QuestionsType
from convertor import convertor
from utils.html.html_string_page import html_string_page
import threading
import json
import traceback

class Api:
    def __init__(self):
        self._window = None

    def process_form(self, filename, file_base64, question_type_html, platform_type_html, are_questions_random, discipline_code="", grade_code=""):
        thread = threading.Thread(
            target=self._background_task,
            args=(filename, file_base64, question_type_html, platform_type_html, are_questions_random, discipline_code, grade_code)
        )
        thread.start()

    def _background_task(self, filename, file_base64, question_type_html, platform_type_html, are_questions_random, discipline_code, grade_code):
        try:
            file_bytes = base64.b64decode(file_base64)
            file_stream = BytesIO(file_bytes)
            question_type = QuestionsType.EDUCA if question_type_html == "EDUCA" else QuestionsType.PPD
            platform_type = PlatformType.AVA if platform_type_html == "AVA" else PlatformType.PLATAFORMA_A

            result = convertor(
                filename=filename,
                file_stream=file_stream,
                are_questions_random=are_questions_random,
                question_type=question_type,
                platform_type=platform_type,
                window=self._window,
                discipline_code=discipline_code,
                grade_code=grade_code)
                        
            buffer = result["csv"]["buffer"]
            if buffer:
                encoded_csv = base64.b64encode(buffer.getvalue()).decode("utf-8")
                result["csv"]["buffer"] = encoded_csv
                        
            self.send_result_to_js({"success": True, "data": result})

        except Exception as e:
            print("--- ERRO NO BACKEND (THREAD) ---")
            traceback.print_exc()
            print("---------------------------------")            
            self.send_result_to_js({"success": False, "error": str(e)})

    def send_result_to_js(self, result):        
        result_json = json.dumps(result)
                
        if self._window:
            self._window.evaluate_js(f'handlePythonResult({result_json})')

def main():
    api = Api()
    window = webview.create_window(
        "Script de questões | NITE",
        html=html_string_page,
        width=600,
        height=400,
        js_api=api
    )
    api._window = window
    webview.start(http_server=True)

if __name__ == "__main__":
    main()