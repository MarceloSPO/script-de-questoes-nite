import streamlit as st
import re
from io import StringIO

st.set_page_config(page_title="BancoMestre.py", layout="centered")
st.title("📄 BancoMestre — Conversor de Questões .TXT para Brightspace CSV")
st.markdown("Envie um `.txt` com questões formatadas e gere um `.csv` compatível com o D2L Brightspace.")

uploaded_file = st.file_uploader("📎 Selecione o arquivo `.txt`", type="txt")

def limpar_bom(texto_bytes):
    return texto_bytes.decode("utf-8-sig")

def limpar_identificador(raw_id):
    return re.sub(r"\s+", "", raw_id.strip())

def extrair_questoes_txt(texto):
    blocos = re.split(r"\*\*[Ii]dentificação da questão\*\*", texto)
    questoes = []

    for bloco in blocos[1:]:
        bloco = bloco.strip()

        id_match = re.search(r"(PPD?_?FE_[^\n]+)", bloco)
        id_questao = limpar_identificador(id_match.group(1)) if id_match else ""

        texto_base_match = re.search(r"\*\*[Tt]exto[- ]?base[\*\:\n]*\s*(.*?)\s*\*\*", bloco, re.DOTALL)
        texto_base = texto_base_match.group(1).strip() if texto_base_match else ""

        enunciado_match = re.search(r"\*\*[Ee]nunciado[\*\:\n]*\s*(.*?)\s*\*\*", bloco, re.DOTALL)
        enunciado = enunciado_match.group(1).strip() if enunciado_match else ""

        alternativas_match = re.search(r"\*\*[Aa]lternativas[\*\:\n]*\s*(.*?)\s*\*\*", bloco, re.DOTALL)
        alternativas_raw = alternativas_match.group(1).strip() if alternativas_match else ""

        gabarito_match = re.search(r"\*\*[Gg]abarito[\*\:\n]*\s*(.*?)(?=\n\*\*|\nCurso:|\Z)", bloco, re.DOTALL)
        gabarito_raw = gabarito_match.group(1).strip() if gabarito_match else ""
        letra_match = re.search(r"\[?([A-E])\]?|Letra\s+([A-E])|Alternativa\s+([A-E])|^([A-E])[).]?", gabarito_raw)
        gabarito_letra = next((g for g in letra_match.groups() if g), "") if letra_match else ""

        feedback_match = re.search(r"\*\*[Ff]eedback[\*\:\n]*\s*(.*?)(?=\nCurso:|\n\*\*|\Z)", bloco, re.DOTALL)
        feedback = feedback_match.group(1).strip() if feedback_match else ""

        alternativas = []
        for linha in alternativas_raw.split("\n"):
            alt_match = re.match(r"^[ \t]*([A-Ea-e])[).:\-]?[ \t]+(.*)", linha.strip())
            if alt_match:
                letra, texto = alt_match.groups()
                alternativas.append((letra.upper(), texto.strip()))

        if id_questao and alternativas and gabarito_letra:
            questoes.append({
                "ID": id_questao,
                "Title": id_questao,  # Descrição Curta
                "QuestionText": f"{texto_base}\n\n{enunciado}",
                "Options": [
                    (100 if letra == gabarito_letra.upper() else 0, texto)
                    for letra, texto in alternativas
                ],
                "Feedback": feedback
            })

    return questoes

def gerar_csv(questoes):
    csv_data = StringIO()
    csv_data.write("//MULTIPLE CHOICE QUESTION TYPE,,,,\n")
    csv_data.write("//Options must include text in column3,,,,\n")

    for q in questoes:
        csv_data.write("NewQuestion,MC,,,\n")
        csv_data.write(f"ID,{q['ID']},,,\n")
        csv_data.write(f"Title,{q['Title']},,,\n")
        csv_data.write(f'QuestionText,"{q["QuestionText"]}",,,\n')
        csv_data.write("Points,1,,,\n")
        csv_data.write("Difficulty,1,,,\n")
        for pontuacao, texto in q["Options"]:
            csv_data.write(f"Option,{pontuacao},{texto},,\n")
        csv_data.write(f'Feedback,"{q["Feedback"]}",,,\n\n')

    return csv_data.getvalue()

if uploaded_file:
    try:
        texto = limpar_bom(uploaded_file.read())
        questoes = extrair_questoes_txt(texto)

        if not questoes:
            st.warning("⚠️ Nenhuma questão foi detectada. Verifique os marcadores ou formatação.")
        else:
            st.success(f"✅ {len(questoes)} questões convertidas com sucesso!")
            csv_content = gerar_csv(questoes)
            st.download_button("⬇️ Baixar CSV", csv_content, "BancoMestre_Brightspace.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {str(e)}")