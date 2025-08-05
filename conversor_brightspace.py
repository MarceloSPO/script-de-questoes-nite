import re
from docx import Document
import os
import csv

def extrair_questoes(docx_path):
    try:
        print("📖 Processando documento Word...")
        doc = Document(docx_path)
        
        questoes = []
        current_questao = None
        
        for tabela in doc.tables:
            # Extrai todo o texto da tabela
            texto_tabela = "\n".join(cell.text.strip() for row in tabela.rows for cell in row.cells if cell.text.strip())
            
            # Verifica se é uma tabela de questão
            if "Identificação da questão" in texto_tabela and "PPD_FE_" in texto_tabela:
                if current_questao:  # Salva a questão anterior antes de começar uma nova
                    if all(k in current_questao for k in ["ID", "QuestionText", "Options", "Gabarito"]):
                        questoes.append(current_questao)
                        print(f"✅ Questão encontrada: {current_questao['ID']}")
                
                # Inicia nova questão
                current_questao = {
                    "ID": "",
                    "QuestionText": "",
                    "Options": [],
                    "Gabarito": "",
                    "Feedback": "",
                    "Title": ""
                }
                
                # Extrai ID da questão
                for cell in [cell for row in tabela.rows for cell in row.cells]:
                    texto = cell.text.strip()
                    if "PPD_FE_" in texto:
                        current_questao["ID"] = texto.replace("**Identificação da questão**", "").strip()
                        # Extrai título da questão (Q01, Q02, etc.)
                        match = re.search(r'_Q(\d+)', current_questao["ID"])
                        if match:
                            current_questao["Title"] = f"Questão {match.group(1)}"
                        break
            
            elif current_questao:  # Se estamos processando uma questão
                # Extrai texto base e enunciado
                if "Texto-base:" in texto_tabela or "Enunciado" in texto_tabela:
                    texto_completo = []
                    in_texto_base = False
                    in_enunciado = False
                    
                    for row in tabela.rows:
                        for cell in row.cells:
                            texto = cell.text.strip()
                            if "Texto-base:" in texto:
                                in_texto_base = True
                                continue
                            elif "Enunciado" in texto:
                                in_texto_base = False
                                in_enunciado = True
                                continue
                            elif "Alternativas" in texto:
                                in_enunciado = False
                                break
                            
                            if in_texto_base or in_enunciado:
                                texto_completo.append(texto)
                    
                    current_questao["QuestionText"] = " ".join(texto_completo)
                
                # Extrai alternativas
                elif "Alternativas" in texto_tabela:
                    current_questao["Options"] = []
                    in_alternativas = False
                    
                    for row in tabela.rows:
                        for cell in row.cells:
                            texto = cell.text.strip()
                            if "Alternativas" in texto:
                                in_alternativas = True
                                continue
                            elif "Gabarito" in texto:
                                in_alternativas = False
                                break
                            
                            if in_alternativas:
                                # Remove marcadores de resposta correta se existirem
                                texto = texto.replace("[", "").replace("]", "").replace("{.mark}", "")
                                match = re.match(r'^([A-E])[).]\s*(.+)$', texto)
                                if match:
                                    current_questao["Options"].append((match.group(1), match.group(2)))
                
                # Extrai gabarito
                elif "Gabarito" in texto_tabela:
                    for row in tabela.rows:
                        for cell in row.cells:
                            texto = cell.text.strip()
                            if "Gabarito" in texto:
                                match = re.search(r'[(\[]([A-E])[)\]]', texto)
                                if match:
                                    current_questao["Gabarito"] = match.group(1)
                                break
                
                # Extrai feedback
                elif "Feedback" in texto_tabela:
                    feedback = []
                    in_feedback = False
                    
                    for row in tabela.rows:
                        for cell in row.cells:
                            texto = cell.text.strip()
                            if "Feedback" in texto:
                                in_feedback = True
                                continue
                            elif in_feedback and not any(x in texto for x in ["Identificação da questão", "PPD_FE_"]):
                                feedback.append(texto)
                    
                    current_questao["Feedback"] = " ".join(feedback)
        
        # Adiciona a última questão processada
        if current_questao and all(k in current_questao for k in ["ID", "QuestionText", "Options", "Gabarito"]):
            questoes.append(current_questao)
            print(f"✅ Questão encontrada: {current_questao['ID']}")
        
        print(f"\n📊 Total de questões válidas: {len(questoes)}")
        return questoes
    
    except Exception as e:
        print(f"❌ Erro durante o processamento: {str(e)}")
        return []

def gerar_csv_brightspace(questoes, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Escreve cabeçalho conforme template Brightspace
            writer.writerow(["NewQuestion","MC","","",""])
            writer.writerow(["ID","","","",""])
            writer.writerow(["Title","","","",""])
            writer.writerow(["QuestionText","","","",""])
            writer.writerow(["Points","","","",""])
            writer.writerow(["Difficulty","","","",""])
            writer.writerow(["Image","","","",""])
            writer.writerow(["Hint","","","",""])
            writer.writerow(["Feedback","","","",""])
            
            for q in questoes:
                # Cabeçalho da questão
                writer.writerow(["NewQuestion","MC","","",""])
                writer.writerow(["ID", q["ID"],"","",""])
                writer.writerow(["Title", q["Title"],"","",""])
                
                # Junta o ID com o texto da questão
                question_text = f"{q['ID']}. {q['QuestionText'].strip()}"
                writer.writerow(["QuestionText", question_text,"","",""])
                
                writer.writerow(["Points","1","","",""])
                writer.writerow(["Difficulty","1","","",""])
                writer.writerow(["Image","","","",""])
                writer.writerow(["Hint","","","",""])
                
                # Alternativas (garante 5 opções)
                opcoes = q["Options"][:5]  # Pega no máximo 5 alternativas
                for letra, texto in opcoes:
                    peso = "100" if letra == q["Gabarito"] else "0"
                    # Remove espaços extras e formata corretamente
                    texto_limpo = ' '.join(texto.split())
                    writer.writerow(["Option", peso, texto_limpo,"",""])
                
                # Preenche com opções vazias se tiver menos de 5
                for _ in range(len(opcoes), 5):
                    writer.writerow(["Option","0"," ","",""])
                
                # Feedback
                feedback_limpo = ' '.join(q["Feedback"].split()) if q["Feedback"] else ""
                writer.writerow(["Feedback", feedback_limpo,"","",""])
                writer.writerow([])  # Linha vazia entre questões
            
        print(f"💾 CSV gerado no formato Brightspace: {output_path}")
        return True
    
    except Exception as e:
        print(f"❌ Falha ao gerar CSV: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔄 Iniciando conversão DOCX para Brightspace CSV")
    
    # Configura caminhos
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCX_FILE = "Agronomia_-_Atividades.docx"
    CSV_FILE = "Questoes_Brightspace.csv"
    
    docx_path = os.path.join(BASE_DIR, DOCX_FILE)
    csv_path = os.path.join(BASE_DIR, CSV_FILE)
    
    print(f"📄 Documento de entrada: {docx_path}")
    print(f"📝 Arquivo de saída: {csv_path}")
    
    if not os.path.exists(docx_path):
        print("\n❌ Arquivo DOCX não encontrado!")
        print("Verifique se o arquivo existe e tem o nome correto:")
        print(f"- Nome esperado: {DOCX_FILE}")
        print(f"- Diretório: {BASE_DIR}")
    else:
        # Processa o documento
        questoes = extrair_questoes(docx_path)
        
        if questoes:
            if gerar_csv_brightspace(questoes, csv_path):
                print(f"\n🎉 Conversão concluída com sucesso!")
                print(f"Total de questões convertidas: {len(questoes)}")
                print("\nInstruções para importar no Brightspace:")
                print("1. Vá para 'Question Bank' no seu curso")
                print("2. Selecione 'Import'")
                print("3. Escolha o arquivo gerado:", CSV_FILE)
                print("4. Confirme os parâmetros de importação")
            else:
                print("\n⚠️ Erro ao gerar arquivo CSV")
        else:
            print("\n⚠️ Nenhuma questão válida foi encontrada")
            
            # Debug avançado
            doc = Document(docx_path)
            if doc.tables:
                print("\nEstrutura da primeira tabela para análise:")
                primeira_tabela = doc.tables[0]
                for i, row in enumerate(primeira_tabela.rows[:3]):  # Mostra apenas 3 linhas para análise
                    print(f"\nLinha {i}:")
                    for j, cell in enumerate(row.cells):
                        texto = cell.text.strip().replace('\n', ' ')[:50]
                        print(f"  Célula {j}: {texto}...")
            else:
                print("O documento não contém tabelas.")