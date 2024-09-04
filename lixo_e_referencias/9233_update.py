from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def iniciar_driver():
    try:
        print("Iniciando o driver do Chrome...")
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        print("Driver iniciado com sucesso.")
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o driver do Chrome: {e}")
        return None


def verificar_situacao(driver, xpath, index=2 ):#manter verificação
    index_novo = 0
    try:
        situacao_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[2]/td[5]/span[2]/span'
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, situacao_xpath)))
        campo_situacao = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, situacao_xpath)))
        campo_situacao_texto = campo_situacao.text
        print(f"Executando verificação na situação da nota fiscal: {campo_situacao_texto}")
        time.sleep(4)
      
#se estiver rejeitada ou em protocolo, pular pra prox nota
        if 'Rejeitada' in campo_situacao_texto or 'Aguardando protocolo' in campo_situacao_texto:
            index_novo += 1#update index
            print(f'verificar se passou para checkbox nº{index}')

            botao_cancelar_xpath = '/html/body/div[6]/div[2]/form/div/div/div[1]/div/div[2]/button'
            botao_cancelar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_cancelar_xpath))
        )#corrigir cenario
            actions = ActionChains(driver)
            actions.move_to_element(botao_cancelar).click().perform()
            print("Processo cancelado.")
            time.sleep(4)
        else:
            print('situação pendente')
    except Exception as e:
        print(f"Situação não capturada: {e}")
        

def selecionar_checkbox_e_campo(driver, index, xpath):
    #verificar situação nota fiscal
    situacao_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[2]/td[5]/span[2]/span'
    print(f"Executando verificação na situação da nota fiscal: {xpath}")
    time.sleep(4)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, situacao_xpath)))
    campo_situacao = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, situacao_xpath)))
    campo_situacao_texto = campo_situacao.text
    print(f"Nota com situação: {campo_situacao_texto}")
    time.sleep(4)
    if 'Pendente'in campo_situacao_texto:
        try:
            print(f"Tentando selecionar a checkbox {index}...")
            checkbox_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{index + index_novo}]/td[1]/div/label'
            campo_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{index + index_novo}]/td[4]'
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
            )
            actions = ActionChains(driver)
            actions.move_to_element(checkbox).click().perform()
            print("Checkbox selecionada com sucesso.")
            time.sleep(0.5)
            campo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, campo_xpath))
            )
            actions.move_to_element(campo).click().perform()
            print("Campo associado selecionado com sucesso.")
        except Exception as e:
            print(f"Erro ao selecionar a checkbox ou campo: {e}")

def determinar_cfop(cep_text):
    cep_prefix = cep_text[:5]
    cep_num = int(cep_prefix.replace("-", ""))
    if (72800 <= cep_num <= 72999) or (73700 <= cep_num <= 76799):
        return 5102
    else:
        return 6108

def desmarcar_checkbox_atual(driver, index):
    try:
        print(f"Tentando desmarcar a checkbox {index}...")
        checkbox_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div/label'
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).click().perform()
        print(f"Checkbox {index} desmarcada.")
    except Exception as e:
        print(f"Erro ao desmarcar checkbox: {e}")

def clicar_no_elemento(driver, xpath):
    print(f"Executando clicar_no_elemento com XPath: {xpath}")
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"Elemento com XPath {xpath} está clicável.")
        actions = ActionChains(driver)
        actions.move_to_element(elemento).click().perform()
        print(f"Elemento com XPath {xpath} clicado com ActionChains.")
    except Exception as e:
        print(f"Erro ao clicar no elemento com ActionChains: {e}")

def processar_itens_nota(driver, cfop):
    item_xpaths = [
        '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[1]/td[1]',
        '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[2]/td[1]',
        '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[3]/td[1]',
        '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[4]/td[1]',
        '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[5]/td[1]',
    ]

    for item_xpath in item_xpaths:
        try:
            item_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, item_xpath))
            )
            print(f"Item encontrado: {item_xpath}")
            
            driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - window.innerHeight * 0.3);", item_element)
            time.sleep(1)
            
            actions = ActionChains(driver)
            actions.move_to_element(item_element).perform()
            time.sleep(1)
            clicar_no_elemento(driver, item_xpath)
            processar_item(driver, cfop, item_xpath)
        except Exception as e:
            print(f"Item não encontrado ou não clicável: {e}")
            break

def processar_item(driver, cfop, item_xpath):
    try:
        print("Tentando selecionar e clicar no produto...")
        novo_campo = driver.find_element(By.XPATH, item_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(novo_campo).click().perform()
        time.sleep(1)

        campo_apagar_xpath = '//*[@id="edValorDescontoItem"]'
        campo_apagar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_apagar_xpath))
        )
        campo_apagar.clear()
        print("Desconto apagado.")

        copiar_codigo_origem_xpath = '/html/body/div[28]/form/div/div/div/div[1]/div[2]/input'
        campo_origem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, copiar_codigo_origem_xpath))
        )
        print("Campo de origem encontrado.")
        copiacodigo = campo_origem.get_attribute("value")
        print(f"Texto copiado: {copiacodigo}")

        campo_destino_xpath = '/html/body/div[28]/form/div/div/div/div[1]/div[1]/input[2]'
        campo_destino = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_destino_xpath))
        )
        print("Campo de destino encontrado.")
        campo_destino.clear()
        campo_destino.send_keys(copiacodigo)
        print(f"Texto colado no elemento com XPath {campo_destino_xpath}: {copiacodigo}")
        time.sleep(2)
        print('Pressionando Enter')
        actions.send_keys(Keys.RETURN).perform()
        time.sleep(1)

        campo_cfop_xpath = '/html/body/div[28]/form/div/div/div/div[3]/div[9]/input'
        campo_cfop = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_cfop_xpath))
        )
        campo_cfop.clear()
        campo_cfop.send_keys(str(cfop))
        print(f"Valor {cfop} colado no campo CFOP.")
        
        salvar_alteracoes_item(driver)

    except Exception as e:
        print(f"Erro ao processar o item: {e}")
        botao_salvar_item_xpath = '/html/body/div[28]/div[1]/button[1]'
        clicar_no_elemento(driver, botao_salvar_item_xpath)

def salvar_alteracoes_item(driver):
    try:
        print("Tentando salvar alterações do item...")
        botao_salvar_xpath = '//*[@id="btnSalvar"]'
        botao_salvar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_xpath))
        )
        botao_salvar.click()
        print("Alterações salvas.")
    except Exception as e:
        print(f"Erro ao salvar alterações do item: {e}")

def main():
    
    driver = iniciar_driver()
    if driver is None:
        return
    
    driver.get('https://www.bling.com.br/notas.fiscais.php#list') # Substitua pela URL real
    xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[2]/td[5]/span[2]/span'
    while True:
        verificar_situacao(driver, xpath, index=2)
        selecionar_checkbox_e_campo(driver, xpath, 2)
        time.sleep(2)
        
        cep_text = driver.find_element(By.XPATH, '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[2]/td[5]').text
        cfop = determinar_cfop(cep_text)
        processar_itens_nota(driver, cfop)
        
        desmarcar_checkbox_atual(driver, 2)
        time.sleep(3)
        break

    driver.quit()

if __name__ == "__main__":
    main()
