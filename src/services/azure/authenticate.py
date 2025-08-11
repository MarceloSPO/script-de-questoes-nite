import os
from dotenv import load_dotenv

import requests

load_dotenv()

def authenticate() -> str | None:
  try:
    tenant_id = os.getenv("AZURE_TENANT_ID")
    ms_uri = os.getenv("MS_AUTH_URL")
    url = f"{ms_uri}/{tenant_id}/oauth2/v2.0/token"

    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET_VALUE")
    
    data = {
      "grant_type": "client_credentials",
      "client_id": client_id,
      "client_secret": client_secret,
      "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(url, data)
    json_res = response.json()

    access_token = json_res["access_token"]

    return access_token
  except requests.RequestException:
    print("Não foi possível realizar a autenticação na Microsoft!")
    return None
