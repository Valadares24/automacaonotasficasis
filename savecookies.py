import requests
import json

# URL do DevTools remoto
devtools_url = "http://localhost:9222/json"

# Obter lista de abas abertas
response = requests.get(devtools_url)
tabs = json.loads(response.text)

# Exibir informações das abas abertas
for tab in tabs:
    print(f"ID: {tab['id']}, URL: {tab['url']}, Título: {tab['title']}")

# Selecione a aba que contém o URL do Bling
bling_tab_id = None
for tab in tabs:
    if "bling.com.br" in tab['url']:
        bling_tab_id = tab['id']
        break

print(f"ID da aba do Bling: {bling_tab_id}")
