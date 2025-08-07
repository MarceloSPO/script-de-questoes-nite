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

### Executando os _scripts_:

- O arquivo principal do projeto é `./src/convertor.py` e para executá-lo basta rodar:

```
python ./src/convertor.py
```

### Questões do EDUCA:

- O formato das questões do EDUCA segue a seguinte estrutura:

1. Um ID no formato: `CCCC_CCCCCC_CCCCCC_CCCCCC_CCCC`;
2. Um enunciado, que pode conter outros tipos de listas;
3. A lista de opções objetivas, onde deverá ser utilizada uma lista organizada por letras (maiúsculas ou minúsculas).
