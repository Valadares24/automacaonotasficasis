from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Função para iniciar o driver do Chrome e conectar à sessão do Chrome Debugger
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Função para verificar o acesso à página
def verificar_acesso_pagina(driver, url):
    try:
        driver.get(url)
        time.sleep(2)  # Esperar 2 segundos para a página carregar
        titulo_pagina = driver.title
        print(f"Título da página acessada: {titulo_pagina}")
        return True
    except Exception as e:
        print(f"Erro ao acessar a página: {e}")
        return False

# Função para selecionar a checkbox e o campo associado
def selecionar_checkbox_e_campo():
    try:
        print("Tentando selecionar a primeira checkbox...")
        # Selecionar a primeira checkbox
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'  #XPath da checkbox
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        checkbox.click()
        print("Checkbox selecionada com sucesso.")
        # Esperar 2 segundos
        time.sleep(2)
        print("Tentando selecionar o campo associado à checkbox...")
        # Selecionar o campo associado à checkbox
        campo_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[4]/span[2]'  # Preencher com o XPath do campo da nota
        campo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        campo.click()
        print("Campo associado selecionado com sucesso.")
        
    except Exception as e:
        print(f"Erro ao selecionar a checkbox ou campo: {e}")

# Função para validar o CFOP da nota olhando o CEP dela
def validar_cfop(driver):
    cep_xpath = '//*[@id="uf"]'  # Preencher com o XPath do campo de CEP
    cep_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, cep_xpath))
    )
    cep = cep_field.get_attribute("value")
    cfop = "5102" if cep.startswith("72") else "6108"
    return cfop

# Função para rolar a página para uma altura de 10%
def rolar_pagina(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.1);")

# Função para selecionar o produto da nota fiscal
def selecionar_produto(driver):
    produto_xpath = '####'  # Preencher com o XPath do produto
    produto = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, produto_xpath))
    )
    produto.click()

# Função para colar o código do produto no campo ao lado
def colar_codigo_produto(driver, codigo):
    origem_xpath = '####'  # Preencher com o XPath do campo de origem
    destino_id = '####'  # Preencher com o ID do campo de destino
    
    campo_origem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, origem_xpath))
    )
    copiacodigo = campo_origem.get_attribute("value")

    campo_destino = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, destino_id))
    )
    campo_destino.clear()
    campo_destino.send_keys(copiacodigo)

    campo_destino.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)
    
    produto_xpath = '####'  # Preencher com o XPath do produto após abrir o campo de colagem
    produto = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, produto_xpath))
    )
    produto.click()

# Função para colar o valor do CFOP no campo correspondente
def colar_valor_cfop(driver, cfop):
    cfop_xpath = '####'  # Preencher com o XPath do campo de CFOP
    campo_cfop = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, cfop_xpath))
    )
    campo_cfop.clear()
    campo_cfop.send_keys(cfop)

# Função para apagar o valor do campo de desconto
def apagar_valor_desconto(driver):
    desconto_id = '####'  # Preencher com o ID do campo de desconto
    campo_desconto = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, desconto_id))
    )
    campo_desconto.clear()

# Função para salvar o item
def salvar_item(driver):
    salvar_item_xpath = '####'  # Preencher com o XPath do botão de salvar item
    botao_salvar_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, salvar_item_xpath))
    )
    botao_salvar_item.click()

# Função para salvar a nota fiscal
def salvar_nota(driver):
    salvar_nota_xpath = '####'  # Preencher com o XPath do botão de salvar nota fiscal
    botao_salvar_nota = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, salvar_nota_xpath))
    )
    botao_salvar_nota.click()

# Função para emitir a nota fiscal
def emitir_nota(driver):
    emitir_xpath = '####'  # Preencher com o XPath do botão de emitir nota fiscal
    botao_emitir = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, emitir_xpath))
    )
    botao_emitir.click()
    time.sleep(20)

# Função para processar uma única nota fiscal
def processar_nota_fiscal(driver):
    try:
        selecionar_checkbox(driver)
        abrir_campo_da_nota(driver)
        cfop = validar_cfop(driver)
        rolar_pagina(driver)
        selecionar_produto(driver)
        colar_codigo_produto(driver, cfop)
        colar_valor_cfop(driver, cfop)
        salvar_item(driver)
        time.sleep(2)
        abrir_campo_da_nota(driver)
        apagar_valor_desconto(driver)
        salvar_item(driver)
        time.sleep(2)
        salvar_nota(driver)
        emitir_nota(driver)
        return True
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False

# Função para verificar se há mais notas fiscais a serem processadas
def existem_mais_notas_fiscais(driver):
    try:
        checkbox_xpath = '####'  # Preencher com o XPath da checkbox
        elemento = driver.find_element(By.XPATH, checkbox_xpath)
        return elemento is not None
    except:
        return False

# Função principal
def main():
    driver = iniciar_driver()
    url = "https://www.bling.com.br/notas.fiscais.php#list"
    if verificar_acesso_pagina(driver, url):
        print("Página acessada com sucesso.")
        while existem_mais_notas_fiscais(driver):
            sucesso = processar_nota_fiscal(driver)
            if not sucesso:
                break
            time.sleep(2)  # Delay entre cada iteração do loop
        print("Todas as notas fiscais foram processadas.")
    else:
        print("Falha ao acessar a página.")
    driver.quit()

if __name__ == "__main__":
    main()
