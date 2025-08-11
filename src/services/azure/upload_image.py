import os

import requests

from src.services.azure.authenticate import authenticate

def upload_image():
  try:     
    ACCESS_TOKEN = authenticate()

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    filename = "exemplo_08_08_2025_928.png"
    file_path = fr".\output\{filename}"

    with open(file_path, "rb") as f:
        upload_url = "https://graph.microsoft.com/v1.0/me/drive/root:/{filename}:/content"
        resp = requests.put(upload_url, headers=headers, data=f)
    resp.raise_for_status()

    file_id = resp.json()['id']
    
    link_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/createLink"
    payload = {
        "type": "view",
        "scope": "anonymous"
    }
    link_resp = requests.post(link_url, headers={**headers, "Content-Type": "application/json"}, json=payload)
    link_resp.raise_for_status()

    print("Link público:", link_resp.json()['link']['webUrl'])
  except requests.RequestException as e:
     print("Não foi possível realizar o upload da sua imagem!",e)

upload_image()