from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  # Corrected import statement
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

def acessar_pagina(driver, url):
    try:
        print(f"Acessando a página: {url}")
        driver.get(url)
        print(f"Página {url} acessada com sucesso.")
    except Exception as e:
        print(f"Erro ao acessar a página {url}: {e}")

def selecionar_checkbox_e_campo(driver, index):
    try:
        print(f"Tentando selecionar a checkbox {index}...")
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
        campo_xpath = f'/html/body/div[6]/div[6]/div[2]/div[7]/table/tbody/tr[{index}]/td[4]'
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        checkbox.click()
        print("Checkbox selecionada com sucesso.")
        time.sleep(2)
        campo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        campo.click()
        print("Campo associado selecionado com sucesso.")
    except Exception as e:
        print("erro no acesso da checkbox")

        raise e

def determinar_cfop(cep_text):
    cep_prefix = cep_text[:5]
    cep_num = int(cep_prefix.replace("-", ""))
    if (72800 <= cep_num <= 72999) or (73700 <= cep_num <= 76799):
        return 5102
    else:
        return 6108

def clicar_no_elemento(driver, xpath):
    print(f"Executando clicar_no_elemento com XPath: {xpath}")
    try:
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"Elemento com XPath {xpath} está clicável.")
        time.sleep(2)
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
            driver.execute_script("window.scrollTo(0, 0);")  # Rolar a página para o topo
            clicar_no_elemento(driver, item_xpath)
            
            # Processar o item
            processar_item(driver, cfop)
        except Exception as e:
            print(f"Item não encontrado ou não clicável: {e}")
            break

def processar_item(driver, cfop):
    try:
        print("Tentando selecionar e clicar no produto...")
        novo_campo_xpath = '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[1]/td[9]/span[5]'
        novo_campo = driver.find_element(By.XPATH, novo_campo_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(novo_campo).click().perform()
        time.sleep(3)

        copiar_codigo_origem_xpath = '//*[@id="edCodigo"]'
        campo_origem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, copiar_codigo_origem_xpath))
        )
        print("Campo de origem encontrado.")
        copiacodigo = campo_origem.get_attribute("value")
        print(f"Texto copiado: {copiacodigo}")

        campo_destino_id = 'edDescricao'
        campo_destino = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, campo_destino_id))
        )
        print("Campo de destino encontrado.")
        campo_destino.clear()
        campo_destino.send_keys(copiacodigo)
        print(f"Texto colado no elemento com ID {campo_destino_id}: {copiacodigo}")

        campo_destino.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        
        campo_produto_xpath = '/html/body/ul[3]/li/a'
        campo_produto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_produto_xpath))
        )
        campo_produto.click()
        print(f"Campo de texto 'produto' com XPath {campo_produto_xpath} clicado.")

        campo_cfop_xpath = '/html/body/div[28]/form/div/div/div/div[3]/div[9]/input'
        campo_cfop = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_cfop_xpath))
        )
        time.sleep(2)
        campo_cfop.clear()
        campo_cfop.send_keys(str(cfop))
        print(f"Valor {cfop} colado no campo CFOP.")
        
        # Salvar alterações no item
        salvar_alteracoes_item(driver)

        # Abrir item novamente
        clicar_no_elemento(driver, novo_campo_xpath)

        # Apagar desconto
        campo_apagar_xpath = '//*[@id="edValorDescontoItem"]'
        time.sleep(1.2)
        campo_apagar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_apagar_xpath))
        )
        campo_apagar.clear()
        print("Desconto apagado.")
        
        # Salvar alterações no item novamente
        salvar_alteracoes_item(driver)

    except Exception as e:
        print(f"Erro ao processar o item: {e}")

def salvar_alteracoes_item(driver):
    try:
        print("Tentando salvar as alterações no item da nota...")
        botao_salvar_item_xpath = '/html/body/div[28]/div[2]/div/button'
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao salvar as alterações no item da nota: {e}")

def processar_nota_fiscal(driver, index):
    try:
        selecionar_checkbox_e_campo(driver, index)
        time.sleep(2)
        
        print("Iniciando a captura do CEP...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        cep_xpath = '/html/body/div[6]/div[2]/form/div/div/div[63]/div[3]/div/input'
        cep_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, cep_xpath))
        )
        time.sleep(2)
        cep_text = cep_field.get_attribute("value")
        cfop = determinar_cfop(cep_text)
        print(f"Valor de CFOP determinado: {cfop}")
        time.sleep(2)

        # Processar itens da nota fiscal
        processar_itens_nota(driver, cfop)

        print("Tentando salvar as alterações na nota...")
        botao_salvar_nota_xpath = '//*[@id="botaoSalvar"]'
        botao_salvar_nota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_nota_xpath))
        )
        botao_salvar_nota.click()
        print("Alterações na nota salvas com sucesso.")
        time.sleep(2)

        if verificar_erro_salvamento(driver):
            print("Erro detectado após salvar a nota.")
            cancelar_processo(driver)
            desmarcar_checkbox_atual(driver, index)
            return True, index + 1
        else:
            emitir_nota_fiscal(driver)
            return False, index

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        cancelar_processo(driver)
        desmarcar_checkbox_atual(driver, index)
        return True, index + 1

def emitir_nota_fiscal(driver):
    try:
        print("Tentando enviar a nota salva")
        botao_enviar_nota_xpath = '//*[@id="container"]/div[3]/div[2]/div/div[1]/button[1]/span[2]'
        botao_enviar_nota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_enviar_nota_xpath))
        )
        botao_enviar_nota.click()
        print("Nota enviada com sucesso.")
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao enviar a nota: {e}")

    try:
        print("Tentando imprimir a nota salva")
        botao_imprimir_nota_xpath = '//*[@id="notaAcao"]'
        botao_imprimir_nota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_imprimir_nota_xpath))
        )
        botao_imprimir_nota.click()
        print("Nota enviada para impressão.")
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao enviar a nota para impressão: {e}")

    try:
        print("Validar envio da nota salva")
        time.sleep(25)
        botao_validar_envio_xpath = '//*[@id="notaAcao"]'
        botao_validar_envio = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, botao_validar_envio_xpath))
        )
        botao_validar_envio.click()
        print("Envio validado com sucesso.")
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao validar envio: {e}")

def verificar_erro_salvamento(driver):
    try:
        print("Verificando mensagem de erro após salvar a nota...")
        mensagem_erro_xpath = '//*[@id="mensagem"]/p[1]'
        mensagem_erro = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, mensagem_erro_xpath))
        ).text
        if mensagem_erro == "Não foi possível salvar a Nota Fiscal":
            print("Mensagem de erro detectada: Não foi possível salvar a Nota Fiscal")
            return True
        return False
    except Exception as e:
        print(f"Erro ao verificar mensagem de erro: {e}")
        return False

def cancelar_processo(driver):
    try:
        print("Tentando cancelar o processo...")
        botao_cancelar_xpath = '/html/body/div[6]/div[2]/form/div/div/div[1]/div/div[2]/button'
        botao_cancelar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_cancelar_xpath))
        )
        botao_cancelar.click()
        print("Processo cancelado.")
    except Exception as e:
        print(f"Erro ao cancelar o processo: {e}")

def desmarcar_checkbox_atual(driver, index):
    try:
        print(f"Tentando desmarcar a checkbox {index}...")
        checkbox_xpath = f'/html/body/div[6]/div[6]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div/label'
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        checkbox.click()
        print(f"Checkbox {index} desmarcada.")
    except Exception as e:
        print(f"Erro ao desmarcar checkbox: {e}")

def existem_mais_notas_fiscais(driver):
    try:
        checkbox_xpath = '/html/body/div[6]/div[6]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, checkbox_xpath))
        )
        return True
    except:
        return False

def print_summary(success_count, error_count):
    print(f"Notas Fiscais emitidas com sucesso: {success_count}")
    print(f"Notas Fiscais com erros: {error_count}")

def main():
    driver = iniciar_driver()
    if driver is not None:
        acessar_pagina(driver, "https://www.bling.com.br/notas.fiscais.php#list")
        success_count = 0
        error_count = 0
        index = 1
        while existem_mais_notas_fiscais(driver):
            try:
                erro, proximo_index = processar_nota_fiscal(driver, index)
                if erro:
                    error_count += 1
                else:
                    success_count += 1
                index = proximo_index
            except Exception as e:
                print(f"Ocorreu um erro ao processar a nota fiscal {index}: {e}")
                error_count += 1
                index += 1
        print_summary(success_count, error_count)
        driver.quit()
    else:
        print("Não foi possível iniciar o driver.")

if __name__ == "__main__":
    main()
