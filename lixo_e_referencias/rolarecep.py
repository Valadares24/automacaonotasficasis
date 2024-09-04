from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar opções do Chrome para depuração remota
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Inicializar o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Capturar o ID da aba aberta
current_window_handle = driver.current_window_handle
print("ID da aba atual:", current_window_handle)

# Lista de todas as abas abertas
window_handles = driver.window_handles
print("IDs de todas as abas abertas:", window_handles)

# Certifique-se de que você está na página correta
expected_url = "https://www.bling.com.br/notas.fiscais.php#list"
if driver.current_url != expected_url:
    print("Você não está na página esperada. Verifique a URL e tente novamente.")
    driver.quit()
    exit()

# Esperar que a página carregue (se necessário)
time.sleep(5)

# Rolar a página para baixo
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Selecionar o campo com ID 'cep'
cep_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "cep"))
)

# Esperar 2 segundos
time.sleep(2)

# Selecionar o campo com a classe 'title-form'
title_form_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "title-form"))
)

# Selecionar o campo de texto no ID 'cep'
cep_text = cep_field.get_attribute("value")

# Criar a variável 'cfop' com base no conteúdo do texto do campo 'cep'
if cep_text.startswith("72") or cep_text.startswith("74"):
    cfop = 5102
else:
    cfop = 6108

print("Valor de cfop:", cfop)

# Selecionar o botão com a classe especificada e clicar nele
close_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ui-button.ui-corner-all.ui-widget.ui-button-icon-only.ui-dialog-titlebar-close"))
)
close_button.click()

# Fechar o navegador após a interação (opcional)
# driver.quit()
