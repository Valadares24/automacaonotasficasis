import requests
import json
import subprocess

# Iniciar o Chrome com depuração remota
def iniciar_chrome_com_debug():
    subprocess.Popen(
        [
            "chrome.exe",
            "--remote-debugging-port=9222",
            "--user-data-dir=C:/ChromeProfile"
        ]
    )

# Verificar as abas abertas no Chrome
def verificar_abas_abertas():
    try:
        devtools_url = "http://localhost:9222/json"
        response = requests.get(devtools_url)
        tabs = json.loads(response.text)

        for tab in tabs:
            print(f"ID: {tab['id']}, URL: {tab['url']}, Título: {tab['title']}")

        # Selecione a aba que contém o URL do Bling
        bling_tab_id = None
        for tab in tabs:
            if "bling.com.br" in tab['url']:
                bling_tab_id = tab['id']
                break

        print(f"ID da aba do Bling: {bling_tab_id}")
        return bling_tab_id
    except requests.exceptions.ConnectionError as e:
        print(f"Erro de conexão: {e}")
        return None

if __name__ == "__main__":
    iniciar_chrome_com_debug()
    time.sleep(5)  # Aguardar alguns segundos para o Chrome iniciar
    bling_tab_id = verificar_abas_abertas()
    if bling_tab_id:
        print("Aba do Bling encontrada.")
    else:
        print("Aba do Bling não encontrada.")
