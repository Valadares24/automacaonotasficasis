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
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
        driver = webdriver.Chrome(options=chrome_options)
        print("Driver iniciado com sucesso.")
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o driver do Chrome: {e}")
        return None


def selecionar_checkbox_e_campo(driver, index):
    try:
        print(f"Tentando selecionar a checkbox {index}...")
        checkbox_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{10}]/td[1]/div/label'
        campo_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{10}]/td[4]'
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).click().perform()
        print("Checkbox selecionada com sucesso.")
        time.sleep(.5)
        campo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        actions.move_to_element(campo).click().perform()
        print("Campo associado selecionado com sucesso.")
    except Exception as e:
        print(f"Erro ao selecionar a checkbox ou campo: {e}")
        raise e

def determinar_cfop(cep_text):
    cep_prefix = cep_text[:5]
    cep_num = int(cep_prefix.replace("-", ""))
    if (72800 <= cep_num <= 72999) or (73700 <= cep_num <= 76799):
        return 5102
    else:
        return 6108

def desmarcar_checkbox_atual(driver, index):#desmarcar
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
        #time.sleep(1)
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
            
            # Rolar a página para 30% acima da posição do elemento
            driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - window.innerHeight * 0.3);", item_element)
            time.sleep(1)  # Espera um curto período para garantir que a rolagem seja concluída
            
            # Usar ActionChains para garantir que o elemento esteja visível e interagível
            actions = ActionChains(driver)
            actions.move_to_element(item_element).perform()
            time.sleep(1)  # Espera um curto período para garantir que o movimento seja concluído

            clicar_no_elemento(driver, item_xpath)
            
            # Processar o item
            processar_item(driver, cfop, item_xpath)
        except Exception as e:
            print(f"Item não encontrado ou não clicável: {e}")
            break  # Se um item não for encontrado, sai do loop e continua o processamento

def processar_item(driver, cfop, item_xpath):
    try:
        #selecionar item 
        print("Tentando selecionar e clicar no produto...")
        novo_campo = driver.find_element(By.XPATH, item_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(novo_campo).click().perform()
        time.sleep(1)

        # Apagar desconto
        campo_apagar_xpath = '//*[@id="edValorDescontoItem"]'
        #time.sleep(1)
        campo_apagar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_apagar_xpath))
        )
        campo_apagar.clear()
        print("Desconto apagado.")

        #copiar codigo origem item
        copiar_codigo_origem_xpath = '/html/body/div[28]/form/div/div/div/div[1]/div[2]/input'
        campo_origem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, copiar_codigo_origem_xpath))
        )
        print("Campo de origem encontrado.")
        copiacodigo = campo_origem.get_attribute("value")
        print(f"Texto copiado: {copiacodigo}")

        #campo destino codigo item
        campo_destino_xpath = '/html/body/div[28]/form/div/div/div/div[1]/div[1]/input[2]'
        campo_destino = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_destino_xpath))
        )
        
        print("Campo de destino encontrado.")#codigo produto
        campo_destino.clear()
        campo_destino.send_keys(copiacodigo)
        print(f"Texto colado no elemento com ID {campo_destino_xpath}: {copiacodigo}")
        time.sleep(2)
        # Pressionar enter para baixo uma vez
        print('Pressionando Enter')
        actions = ActionChains(driver)
        actions.send_keys(Keys.RETURN).perform()
        time.sleep(1)
        

        campo_cfop_xpath = '/html/body/div[28]/form/div/div/div/div[3]/div[9]/input'
        campo_cfop = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_cfop_xpath))
        )
        #time.sleep(1)
        campo_cfop.clear()
        campo_cfop.send_keys(str(cfop))
        print(f"Valor {cfop} colado no campo CFOP.")
        
        # Salvar alterações no item
        salvar_alteracoes_item(driver)

        # Abrir item novamente
        '''clicar_no_elemento(driver, item_xpath)'''

        
        
        # Salvar alterações no item novamente
        '''salvar_alteracoes_item(driver)'''

    except Exception as e:
        print(f"Erro ao processar o item: {e}")
        #primeiro salvar o item da nota
        botao_salvar_item_xpath = '/html/body/div[28]/div[2]/div/button'
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_item).click().perform()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(1)
        #cancela a emissao dessa nota
        print("Tentando cancelar o processo...")
        botao_cancelar_xpath = '/html/body/div[6]/div[2]/form/div/div/div[1]/div/div[2]/button'
        botao_cancelar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_cancelar_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_cancelar).click().perform()
        print("Processo cancelado.")
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
        
        

def salvar_alteracoes_item(driver):
    try:
        time.sleep(1)
        print("Tentando salvar as alterações no item da nota...")
        botao_salvar_item_xpath = '/html/body/div[28]/div[2]/div/button'
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_item).click().perform()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao salvar as alterações no item da nota: {e}")

def processar_nota_fiscal(driver, index):
    try:
        selecionar_checkbox_e_campo(driver, index)
        #time.sleep(1)
        
        print("Iniciando a captura do CEP...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        cep_xpath = '/html/body/div[6]/div[2]/form/div/div/div[30]/div/input'
        cep_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, cep_xpath))
        )
        time.sleep(1)
        cep_text = cep_field.get_attribute("value")
        cfop = determinar_cfop(cep_text)
        print(f"Valor de CFOP determinado: {cfop}")
        #time.sleep(1)

        # Processar itens da nota fiscal
        processar_itens_nota(driver, cfop)

        print("Tentando salvar as alterações na nota...")
        botao_salvar_nota_xpath = '/html/body/div[6]/div[2]/form/div/div/div[1]/div/div[3]/button'
        botao_salvar_nota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_nota_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_nota).click().perform()
        print("Alterações na nota salvas com sucesso.")
        time.sleep(1.5)

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
        time.sleep(1.5)
        print("Tentando enviar a nota salva")#botao de enviar nota
        botao_enviar_nota_xpath = '/html/body/div[6]/div[8]/div[3]/div[2]/div/div[1]/button[1]/span[1]'
        botao_enviar_nota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_enviar_nota_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_enviar_nota).click().perform()
        print("Nota enviada com sucesso.")
        
    except Exception as e:
        print(f"Erro ao enviar a nota: {e}")

    try:
        time.sleep(1)
        print("Tentando imprimir a nota salva")
        botao_imprimir_nota_xpath = '/html/body/div[28]/div[3]/div/button'#enviar selecionado2
        botao_imprimir_nota = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_imprimir_nota_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_imprimir_nota).click().perform()
        print("Nota enviada para impressão.")
        #time.sleep(12)

    except Exception as e:
        print(f"Erro ao enviar a nota para impressão: {e}")

    try:#check
        print('verificar condição de encerramento')
            # Obtém o elemento e extrai o texto
        
        mensagem_verificar_xpath = '/html/body/div[28]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/span'
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, mensagem_verificar_xpath))
    )
        mensagem_verificar_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,  mensagem_verificar_xpath))
        )
        botao_imprimir_final_xpath = '/html/body/div[28]/div[3]/div/button'
        botao_imprimir_final = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, botao_imprimir_final_xpath)))
        mensagem_verificar = mensagem_verificar_element.text
        print(f"mensagem_verificar: {mensagem_verificar}")
        #time.sleep(2)

        while True:  # Loop infinito até que a condição seja satisfeita
            print('Entramos no bloco de verificação')
            if 'Notas fiscais eletrônicas autorizadas com sucesso' in mensagem_verificar or 'Não há nada para ser feito' in mensagem_verificar:
                actions = ActionChains(driver)
                actions.move_to_element(botao_imprimir_final).click().perform()
                print('Sucesso na emissão')
                time.sleep(1)
                break  # Sai do loop se a condição for satisfeita

            elif 'Notas fiscais eletrônicas não foram validadas' in mensagem_verificar:
                print('Emissão não concluída')
                botao_erro_nota_xpath = '/html/body/div[28]/div[3]/div/button'
                botao_enviar_nota = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, botao_erro_nota_xpath)))
                actions = ActionChains(driver)
                actions.move_to_element(botao_enviar_nota).click().perform()
                time.sleep(2)
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


                # Você pode atualizar ou verificar a 'mensagem_verificar' novamente aqui
                mensagem_verificar = driver.find_element(By.XPATH, "xpath_da_mensagem").text  # Supondo que você tenha um XPath para a mensagem
            else:
                print("Nenhuma das condições foi satisfeita, tentando novamente...")
                time.sleep(2)  # Espera um tempo antes de tentar novamente

#xpath pra encerrar a impressao /html/body/div[28]/div[3]/div/button
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
        actions = ActionChains(driver)
        actions.move_to_element(botao_cancelar).click().perform()
        print("Processo cancelado.")
    except Exception as e:
        print(f"Erro ao cancelar o processo: {e}")


def existem_mais_notas_fiscais(driver):
    try:
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
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
        processar_nota_fiscal(driver, 1)#novo
        driver.get("https://www.bling.com.br/notas.fiscais.php#list")  # Abrir a página específica
        success_count = 0
        error_count = 0
        index = 1
        while True:
            try:
                if not existem_mais_notas_fiscais(driver):
                    break
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
