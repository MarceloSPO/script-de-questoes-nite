### Configurar `venv` no Python

1. Criando a pasta da `venv`:

```bash
python -m venv venv
```

2. Ativando a venv:

```bash
source venv/Scripts/activate
```

---

### Baixando as dependências:

É necessário baixar as bibliotecas abaixo para inicializar o projeto:

```bash
pip install streamlit
```

Gerando os _requirements_:

```bash
pip freeze > requirements.txt
```

> Para baixar as dependências a partir do arquivo gerado, basta rodar: `pip install -r requirements.txt`.

---

### Executando projeto em modo de desenvolvimento:

- Para rodar o esse projeto em modo de desenvolvimento, basta seguir o comando abaixo que simula o arquivo `.exe` que é a build.

```
python ./src/pywebview.py
```

Após rodar o comando acessar [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Questões do EDUCA:

- O formato das questões do EDUCA segue a seguinte estrutura:

1. Um ID no formato: `CCCC_CCCCCC_CCCCCC_CCCCCC_CCCC`;
2. Um enunciado, que pode conter outros tipos de listas;
3. A lista de opções objetivas, onde deverá ser utilizada uma lista organizada por letras (maiúsculas ou minúsculas).

---

### Gerar o executável

Esse é o arquivo final onde as pessoas poderão converter as questões. Para gerar o executável (`.exe`) do projeto, basta executar o comando a seguir:

```bash
pyinstaller --noconsole --onefile --icon="./src/assets/icons/icon.ico" --version-file="version.txt" --add-data "./src/templates/index.html;templates" ./src/pywebview.py
```
