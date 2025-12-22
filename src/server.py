from io import BytesIO
import base64
from flask import Flask, request, jsonify
from enums.platform_types import PlatformType, QuestionsType
from convertor import convertor
from flask_cors import CORS

from utils.html_page import get_html_page


app = Flask(__name__)

CORS(app)
@app.route("/")
def index():  
  html_string = get_html_page()  
  return html_string

@app.route("/process", methods=["POST"])
def process():
  try:
    data = request.get_json()      
    file_name = data.get("fileName")
    base64_file = data.get("base64File")
    question_platform = data.get("questionPlatform")
    question_type = data.get("questionType")
    are_questions_random = data.get("isChecked")
    

    file_bytes = base64.b64decode(base64_file)  
    file_stream = BytesIO(file_bytes) 

    type = QuestionsType.EDUCA if question_type == "EDUCA" else QuestionsType.PPD       
    platform_type = PlatformType.PLATAFORMA_A if question_platform == "plataforma-a" else PlatformType.AVA

    res = convertor(file_name, file_stream, are_questions_random, type, platform_type=platform_type)
    csv_res = res.get("csv", None)
    errors = res.get("errors", [])
        
    if csv_res:
      csv_bytes = csv_res.get("buffer").getvalue().encode("utf-8-sig") 
      csv_b64 = base64.b64encode(csv_bytes).decode("utf-8")

      response = {
        "errors": errors,
        "message": "Arquivo convertido com sucesso",
        "filename": csv_res.get("filename"),
        "file": csv_b64
      }

      return jsonify(response)

    return jsonify({ "message": "Resposta invalida", "errors": [] })  
  except Exception as e:
    print("ERROR", e)
    return jsonify({ "message": "Erro inesperado no servidor!" })
if __name__ == "__main__":
    app.run(debug=True)