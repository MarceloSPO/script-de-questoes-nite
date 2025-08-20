from io import BytesIO
import base64
from flask import Flask, render_template, request, send_file, jsonify
from convertor import QuestionsType, convertor

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
  try:
    data = request.get_json()      
    file_name = data.get("fileName")
    base64_file = data.get("base64File")
    question_type = data.get("questionType")
    are_questions_random = data.get("isChecked")
    

    file_bytes = base64.b64decode(base64_file)  
    file_stream = BytesIO(file_bytes) 

    type = QuestionsType.EDUCA if question_type == "EDUCA" else QuestionsType.PPD                  

    res = convertor(file_name, file_stream, are_questions_random, type)
    csv_res = res.get("csv", None)
        
    if csv_res:
      return send_file(
        BytesIO(csv_res.get("buffer").getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=csv_res.get("filename")
      )
    return jsonify({ "message": "Resposta invalida" })  
  except Exception as e:
    print("ERROR", e)
    return jsonify({ "message": "Erro inesperado no servidor!" })
if __name__ == "__main__":
    app.run(debug=True)