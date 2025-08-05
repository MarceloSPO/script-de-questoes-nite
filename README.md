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
