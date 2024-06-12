from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
print("42213A7CBD6DBF98351677B4BAEC31DD", current_window_handle)

# Lista de todas as abas abertas
window_handles = driver.window_handles
print("42213A7CBD6DBF98351677B4BAEC31DD", window_handles)

# Certifique-se de que você está na página correta
expected_url = "https://www.bling.com.br/notas.fiscais.php#list"
if driver.current_url != expected_url:
    print("Você não está na página esperada. Verifique a URL e tente novamente.")
    driver.quit()
    exit()

# Esperar que a página carregue (se necessário)
time.sleep(5)

# Função para selecionar a checkbox e o campo associado
def selecionar_checkbox_e_campo():
    try:
        # Selecionar a primeira checkbox
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        checkbox.click()
        print("Checkbox selecionada.")
        
        # Esperar 2 segundos
        time.sleep(2)
        
        # Selecionar o campo associado à checkbox
        campo_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[3]/span[2]'
        campo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        campo.click()
        print("Campo associado selecionado.")
        
    except Exception as e:
        print(f"Erro ao selecionar a checkbox ou campo: {e}")

# Executa a função para selecionar a checkbox e o campo associado
selecionar_checkbox_e_campo()

time.sleep(4)
######### BLOCO DE INTERAÇÃO COM CEP E DETERMINAÇÃO DE CFOP #######################################################
# Rolar a página para baixo
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Forneça o XPath para o campo "cep"
cep_xpath = '/html/body/div[6]/div[2]/form/div/div/div[63]/div[3]/div/input'  # Substitua pelo XPath do campo "cep"

# Selecionar o campo com XPath fornecido
cep_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, cep_xpath))
)

# Esperar 2 segundos
time.sleep(2)

# Selecionar o campo com a classe 'title-form'
title_form_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "title-form"))
)

# Selecionar o campo de texto no XPath 'cep'
cep_text = cep_field.get_attribute("value")
# Leitura das duas primeiras casas do CEP
cep_prefix = cep_text[:2]
print(f"As duas primeiras casas do CEP são: {cep_prefix}")

# Criar a variável 'cfop' com base no conteúdo do texto do campo 'cep'
if cep_prefix.isdigit() and 72 <= int(cep_prefix) <= 76:
    cfop = 5102
else:
    cfop = 6108

print("Valor de cfop:", cfop)

# Selecionar o botão com a classe especificada e clicar nele
'''close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "ui-button.ui-corner-all.ui-widget.ui-button-icon-only.ui-dialog-titlebar-close"))
) 
close_button.click()'''
######### FIM DO BLOCO DE INTERAÇÃO COM CEP E DETERMINAÇÃO DE CFOP ###########################################################

time.sleep(2)

######### BLOCO DE CLIQUE ADICIONAL #########



######### BLOCO DE CLIQUE ADICIONAL (PARTE 1: ROLAR ATÉ O ELEMENTO) #########
# Forneça o XPath para o novo campo a ser clicado
novo_campo_xpath = '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[1]/td[1]'
print(f"XPath fornecido para o novo campo: {novo_campo_xpath}")

# Função para rolar até o elemento especificado pelo XPath
def rolar_para_elemento(driver, xpath):
    print(f"Executando rolar_para_elemento com XPath: {novo_campo_xpath}")
    try:
        # Esperar que o elemento esteja presente na página
        elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, novo_campo_xpath))
        )
        print(f"Elemento com XPath {novo_campo_xpath} encontrado.")

         # Rolar a página até o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        print(f"Página rolada até o elemento com XPath: {novo_campo_xpath}")

        # Verificar se o elemento está visível
        is_displayed = elemento.is_displayed()
        print(f"Elemento visível: {is_displayed}")
    except Exception as e:
        print(f"Erro ao rolar para o elemento: {e}")
# Função para clicar no elemento especificado pelo XPath
def clicar_no_elemento(driver, novo_campo_xpath):
    print(f"Executando clicar_no_elemento com XPath: {novo_campo_xpath}")
    try:
        # Esperar que o elemento esteja presente e clicável na página
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, novo_campo_xpath))
        )
        print(f"Elemento com XPath {novo_campo_xpath} está clicável.")
        time.sleep(5)
         # Usar JavaScript para clicar no elemento
        driver.execute_script("arguments[0].click();", elemento)
        print(f"Elemento com XPath {novo_campo_xpath} clicado com JavaScript.")
    except Exception as e:
        print(f"Erro ao clicar no elemento com JavaScript: {e}")


# Executar a função para rolar até o elemento
rolar_para_elemento(driver, novo_campo_xpath)
######### FIM DO BLOCO DE CLIQUE ADICIONAL (PARTE 1: ROLAR ATÉ O ELEMENTO) #########
# Esperar 2 segundos para garantir que a rolagem foi concluída
time.sleep(2)

# Executar a função para clicar no elemento
clicar_no_elemento(driver, novo_campo_xpath)
######### FIM DO BLOCO DE CLIQUE ADICIONAL (PARTE 2: clicar no ELEMENTO) #########


print("Aguardando novas instruções ou ações manuais...")
# Aguarda indefinidamente para permitir interação manual ou futuras instruções
while True:
    time.sleep(1)

