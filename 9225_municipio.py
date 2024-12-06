from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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

lista_erros = []
    
def selecionar_checkbox_e_campo(driver, index):
    print('entrou - bloco de selecao nfs')
    time.sleep(1)
    try:

        global campo_situacao_xpath
        global campo_situacao
        global status_campo_situacao
        global checkbox

        campo_situacao_xpath = f'/html/body/div[7]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[5]/span[2]/span'
        campo_situacao = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, campo_situacao_xpath)))
        status_campo_situacao = campo_situacao.text
        
        try:
            print(f'status da nota fiscal atual:{status_campo_situacao}''\n')
        
            if  status_campo_situacao != "Pendente":
                return False, index + 1
            else: 
                try:
                    print(f"Tentando selecionar a checkbox {index}...")
                    checkbox_xpath = f'/html/body/div[7]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div'                          
                    checkbox = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
                    print(f"Checkbox localizada: tag_name={checkbox.tag_name}, location={checkbox.location}, size={checkbox.size}")
                    actions = ActionChains(driver)
                    actions.move_to_element(checkbox).click().perform()
                    print("Checkbox selecionada com sucesso.")
                except NoSuchElementException:
                    print(f"Tentando selecionar a checkbox {index}...")
                    checkbox_xpath = f'/html/body/div[8]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div'                          
                    checkbox = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
                    print(f"Checkbox localizada: tag_name={checkbox.tag_name}, location={checkbox.location}, size={checkbox.size}")
                    actions = ActionChains(driver)
                    actions.move_to_element(checkbox).click().perform()
                    print("Checkbox selecionada com sucesso.")

                try:
                    campo_xpath = f'/html/body/div[7]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[4]'
                    campo = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, campo_xpath)))
                    actions.move_to_element(campo).click().perform()
                    print("Campo associado selecionado com sucesso.")
                except NoSuchElementException:
                    campo_xpath = f'/html/body/div[8]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[4]'
                    campo = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, campo_xpath)))
                    actions.move_to_element(campo).click().perform()
                    print("Campo associado selecionado com sucesso.")
                return True
            
        except Exception as e:
            print(f"Erro ao selecionar a checkbox ou campo: {e}")
            raise e
                
            
    except Exception as e:
        print(f"Erro ao selecionar a checkbox ou campo: {e}")
        raise e

def determinar_cfop(cep_text):
    time.sleep(2)
    #cep_text = WebDriverWait(cep_text, 300).until(EC.element_to_be_clickable((By.XPATH, cep_text)))
    cep_prefix = cep_text[:5]
    cep_num = int(cep_prefix.replace("-", ""))
    print(cep_num)
    if (72800 <= cep_num <= 72999) or (73700 <= cep_num <= 76799):
        return 5102
    else:
        return 6108

def desmarcar_checkbox_atual(driver, index):
    try:
        time.sleep(5)
        print(f"Desmarcando a checkbox {index}...")
        checkbox_xpath = f'/html/body/div[7]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div'
        checkbox = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).click().perform()
        print(f"Checkbox {index} desmarcada.")
        time.sleep(3)
        return True, index + 1

    except NoSuchElementException:
        print(f"Desmarcando a checkbox {index}...")
        checkbox_xpath = f'/html/body/div[8]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[5]/span[2]/span'
        checkbox = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).click().perform()

    except Exception as e:
        print(f"Erro ao desmarcar checkbox: {e}")

def clicar_no_item(driver, xpath):
    print(f"Executando clicar_no_item com XPath: {xpath}")
    
    try:
        elemento = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"Elemento com XPath {xpath} está clicável.")
      
        actions = ActionChains(driver)
        actions.move_to_element(elemento).click().perform()
        print(f"Elemento com XPath {xpath} clicado com ActionChains.")
    except Exception as e:
        print(f"Erro ao clicar no elemento com ActionChains: {e}")

def processar_itens_nota(driver, cfop):
    
    item_xpaths = [f'/html/body/div[7]/div[2]/form/div/div/div[42]/table/tbody/tr[{i}]/td[1]' for i in range (1,17)]

    for item_xpath in item_xpaths:
        try:
            item_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, item_xpath))
            )
            print(f"Item encontrado: {item_xpath}")
            
            
            driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - window.innerHeight * 0.3);", item_element)
            time.sleep(1)  
            
            
            actions = ActionChains(driver)
            actions.move_to_element(item_element).perform()
            time.sleep(1)  

            clicar_no_item(driver, item_xpath)
            
            
           
            processar_item(driver, cfop, item_xpath)
        except Exception as e:
            print(f"Item não encontrado ou não clicável: {e}")
            break  

def processar_item(driver, cfop, item_xpath):
    try:

        print("selecionando o produto dentro da lista de 10...")
        novo_campo = driver.find_element(By.XPATH, item_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(novo_campo).click().perform()
        
        campo_apagar_xpath = '//*[@id="edValorDescontoItem"]'
        campo_apagar = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, campo_apagar_xpath)))
        campo_apagar.clear()
        print("Desconto apagado.")

        #time.sleep(1)
        copiar_codigo_origem_ID = 'edCodigo'#seletor mudado para ID - xpath tava dando muito problema
        campo_origem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, copiar_codigo_origem_ID)))
        print("Campo de origem encontrado.")
        copiacodigo = campo_origem.get_attribute("value")
        print(f"Texto copiado: {copiacodigo}")

       
        campo_destino_ID = 'edDescricao'#ID campo colar codigo produto
        campo_destino = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, campo_destino_ID)))
        print("Campo de destino encontrado.")
        campo_destino.clear()
        campo_destino.send_keys(copiacodigo)
        print(f"Texto colado no elemento com ID {campo_destino_ID}: {copiacodigo}")
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.__class__,tipsyOff ui-autocomplete)))
        time.sleep(3)
        print('Pressionando Enter')
        actions = ActionChains(driver)
        actions.send_keys(Keys.RETURN).perform()
        time.sleep(1)
        
        campo_cfop_ID = 'edCfop'
        campo_cfop = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, campo_cfop_ID)))
        campo_cfop.clear()
        campo_cfop.send_keys(str(cfop))
        print(f"Valor {cfop} colado no campo CFOP.")
        
        salvar_alteracoes_item(driver)

    except Exception as e:
        print(f"Erro ao processar o item: {e}")
        
        cancelar_processo(driver)
        #salvar_alteracoes_item(driver)
        print("Alterações no item da nota salvas com sucesso.")

        time.sleep(1)

        try:
            print("cancelando processo emissão nota...")
            botao_cancelar_com_salvamento_xpath = '/html/body/div[34]/div[2]/div/button'
            botao_cancelar = WebDriverWait(driver, 10).until(#espera até 10 sec para pressionar botao
                EC.element_to_be_clickable((By.XPATH, botao_cancelar_com_salvamento_xpath)))#EC - entender essa sintaxe
            actions = ActionChains(driver)#actionchains para selecionar de forma eficaz - buscar forma mais eficiente(tempo)
            actions.move_to_element(botao_cancelar).click().perform()#move cursor e pressiona botao
            print("Processo cancelado.")#log return processo cancelado
            #time sleep removido, foco n o webdriver wait
            #AVALIAR FUNÇÃO PARA CENARIO DE ERRO GERAL E VERIFICAR POSSIBILIDADE SUBSTITUIR TODO ESSA LOGICA DO BLOCO EXCEPT PELA FUNÇÃO JÁ CRIADA
        except  NoSuchElementException:
            time.sleep(1)
        print("Tentando salvar as alterações no item da nota...")#pipoca
        botao_salvar_item_xpath = '/html/body/div[36]/div[2]/div/button'
        botao_salvar_item = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_item).click().perform()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(1)


def salvar_alteracoes_nota(driver):
    try:
        print("Tentando salvar as alterações na nota...")
        botao_salvar_nota_xpath = '/html/body/div[7]/div[2]/form/div/div/div[1]/div/div[3]/button'
        botao_salvar_nota = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, botao_salvar_nota_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_nota).click().perform()
        print("Alterações na nota salvas com sucesso.")
    except NoSuchElementException:
        print("Tentando salvar as alterações na nota...")
        botao_salvar_nota_xpath = '/html/body/div[8]/div[2]/form/div/div/div[1]/div/div[3]/button'
        botao_salvar_nota = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, botao_salvar_nota_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_nota).click().perform()
        print("Alterações na nota salvas com sucesso.")

def salvar_alteracoes_item(driver):
    try:
        time.sleep(1)
        print("Tentando salvar as alterações no item da nota...")#pipoca
        botao_salvar_item_xpath = '/html/body/div[34]/div[2]/div/button'
        botao_salvar_item = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_item).click().perform()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(1)
    except NoSuchElementException:
        time.sleep(1)
        print("Tentando salvar as alterações no item da nota...")#pipoca
        botao_salvar_item_xpath = '/html/body/div[36]/div[2]/div/button'
        botao_salvar_item = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_salvar_item).click().perform()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao salvar as alterações no item da nota: {e}")

def processar_nota_fiscal(driver, index):
    
        nota_selecionada = selecionar_checkbox_e_campo(driver, index)
        if nota_selecionada:
            selecionar_checkbox_e_campo(driver, index)
            
            print("Iniciando a captura do CEP...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            cep_xpath = '/html/body/div[7]/div[2]/form/div/div/div[30]/div/input'
            cep_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, cep_xpath))
            )
            time.sleep(1)
            cep_text = cep_field.get_attribute("value")
            cfop = determinar_cfop(cep_text)
            print(f"Valor de CFOP determinado: {cfop}")
            #time.sleep(1)

            # Processar itens da nota fiscal
            processar_itens_nota(driver, cfop)

            salvar_alteracoes_nota(driver)
            time.sleep(1)

            if verificar_erro_salvamento(driver):
                print("Erro detectado após salvar a nota.")
                cancelar_processo(driver)
                desmarcar_checkbox_atual(driver, index)
                return True, index + 1
            else:
                emitir_nota_fiscal(driver, index)
                return False, index
            '''if verificar_erro_salvamento(driver):
                if funcao_erro_municipio(driver):
                    print('o script veio para cá - erro municipio')
                    emitir_nota_fiscal(driver, index)
                    #verificar_erro_salvamento(driver):
                    print('Erro de município persiste após tentativa de correção')
                    raise Exception('Erro não corrigido no município')
                    return False, index
                
                else:
                    print('o script veio para cá')
                    print("Erro detectado após salvar a nota.")
                    cancelar_processo(driver)
                    desmarcar_checkbox_atual(driver, index)
                    return True, index + 1
                    
                emitir_nota_fiscal(driver, index)
                    return False, index
                
                except:
                    print('o script veio para cá')
                    print("Erro detectado após salvar a nota.")
                    cancelar_processo(driver)
                    desmarcar_checkbox_atual(driver, index)
                    return True, index + 1
            else:
                print('script nao veio para nenhum caso de erro')
                salvar_alteracoes_nota(driver)
                emitir_nota_fiscal(driver, index)
                return False, index'''
        else:
            print('nota fiscal nao selecionada e pulada')
    
def emitir_nota_fiscal(driver, index):
    print(f'o index atual é {index}')
    try:
        #time.sleep(1)
        print("enviando nota salva p impressao")#botao de enviar nota
        botao_enviar_nota_XPATH = '/html/body/div[7]/div[8]/div[3]/div[2]/div/div[1]/button[1]'
        botao_enviar_nota = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, botao_enviar_nota_XPATH)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_enviar_nota).click().perform()
        print("Nota enviada com sucesso.")
    except NoSuchElementException:
        #time.sleep(1)
        print("enviando nota salva p impressao")#botao de enviar nota
        botao_enviar_nota_XPATH = '/html/body/div[8]/div[8]/div[3]/div[2]/div/div[1]/button[1]'
        botao_enviar_nota = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, botao_enviar_nota_XPATH)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_enviar_nota).click().perform()
        print("Nota enviada com sucesso.")

    except Exception as e:
        print(f"Erro ao enviar a nota: {e}")

    try:
        time.sleep(1)
        print("Pressionar botao para imprimir a nota salva")
        botao_imprimir_nota_xpath = '/html/body/div[34]/div[3]/div/button' 
        botao_imprimir_nota = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, botao_imprimir_nota_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_imprimir_nota).click().perform()
        print("Nota enviada para impressão.")
        time.sleep(1)
    except NoSuchElementException:
        time.sleep(1)
        print("Pressionar botao para imprimir a nota salva")
        botao_imprimir_nota_xpath = '/html/body/div[36]/div[3]/div/button' 
        botao_imprimir_nota = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, botao_imprimir_nota_xpath))
        )
        actions = ActionChains(driver)
        actions.move_to_element(botao_imprimir_nota).click().perform()
        print("Nota enviada para impressão.")
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao enviar a nota para impressão-: {e}")
        
    try:
        print('tentando bloco mensagem')
        time.sleep(2)
        print('verificar condição de encerramento')
           
        while True:  
            time.sleep(5)  
            try:
                mensagem_verificar_xpath = '/html/body/div[34]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/span'#aqui
                print(mensagem_verificar_xpath)
            except NoSuchElementException:
                mensagem_verificar_xpath = '/html/body/div[36]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/span'#aqui
                print(mensagem_verificar_xpath)

            
            mensagem_verificar_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, mensagem_verificar_xpath)))
            print(mensagem_verificar_element)
            mensagem_verificar = mensagem_verificar_element.text
            #time.sleep(5)   
            print(f"mensagem_verificar: {mensagem_verificar}")
            print('conseguimos acessar a variavel mensagem_verificar')
            time.sleep(5)   


        
            botao_imprimir_final_ID = 'notaAcao'
            botao_imprimir_final = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, botao_imprimir_final_ID)))
            
            
            print(f"mensagem_verificar: {mensagem_verificar}")
            print('Entramos no bloco de verificação')

            if 'Notas fiscais eletrônicas autorizadas com sucesso' in mensagem_verificar or 'Não há nada para ser feito' in mensagem_verificar:
                actions = ActionChains(driver)
                actions.move_to_element(botao_imprimir_final).click().perform()
                print('Sucesso na emissão')
                time.sleep(1)
                break  
            else:
                print("Nenhuma das condições foi satisfeita - descartar nota")
                #time.sleep(2) 
                try:
                    botao_fechar_nota_xpath = "/html/body/div[34]/div[1]/button"
                except  NoSuchElementException:
                    botao_fechar_nota_xpath = "/html/body/div[37]/div[1]/button"
                    

                botao_fechar_nota = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, botao_fechar_nota_xpath)))
                actions = ActionChains(driver)
                actions.move_to_element(botao_fechar_nota).click().perform()
                desmarcar_checkbox_atual(driver, index)
                return  index + 1

    except Exception as e:
            print(f"Erro ao validar envio: {e}") 
            
'''def funcao_erro_municipio(driver):
    
    try:
        print('executando alteracao de cadastro relacionada ao municipio')
        time.sleep(3)
        botao_editar_municipio_lapis_xpath = '/html/body/div[7]/div[2]/form/div/div/div[25]/div[1]/span/a[2]/i'
        botao_editar_municipio_lapis = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, botao_editar_municipio_lapis_xpath)))             
        actions = ActionChains(driver)
        actions.move_to_element(botao_editar_municipio_lapis).click().perform()
        print(f'clicado botao de lupa endereço {botao_editar_municipio_lapis_xpath}')
        print('abrindo campo de cadastro do cliente')

        botao_lupa_cep_ID = 'buscaCep'
        botao_lupa_cep = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, botao_lupa_cep_ID))) 
        actions = ActionChains(driver)
        time.sleep(2)
        actions.move_to_element(botao_lupa_cep).click().perform()
        print(f'clicado botao de lupa endereço {botao_lupa_cep_ID}')

        campo_bairro_ID = 'bairro'
        campo_bairro = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, campo_bairro_ID)))
        ActionChains(driver).double_click( campo_bairro).perform()
        campo_bairro.clear()
        print('alterando campo bairro')
        time.sleep(1)
        campo_bairro.send_keys('s/n')

        campo_endereco_ID = 'endereco'
        campo_endereco = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, campo_endereco_ID)))
        ActionChains(driver).double_click(campo_endereco).perform()
        time.sleep(1)
        campo_endereco.clear()
        time.sleep(1)
        print('alterando campo endereco')
        campo_endereco.send_keys('s/n')

        try:
            botao_salvar_novo_cadastro_XPATH = '/html/body/div[34]/div[2]/div/button'
            botao_salvar_novo_cadastro = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, botao_salvar_novo_cadastro_XPATH)))
            actions = ActionChains(driver)
            print('clique botao salvar alteracoes')
            time.sleep(3)
            actions.move_to_element(botao_salvar_novo_cadastro).click().perform()
            print("Verificando mensagem de erro após salvar a nota...")
           
        except NoSuchElementException:
            botao_salvar_novo_cadastro_XPATH = '/html/body/div[36]/div[2]/div/button'
            botao_salvar_novo_cadastro = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, botao_salvar_novo_cadastro_XPATH)))
            actions = ActionChains(driver)
            print('clique botao salvar alteracoes')
            time.sleep(3)
            actions.move_to_element(botao_salvar_novo_cadastro).click().perform()


        time.sleep(3)
        salvar_alteracoes_nota(driver)
        mensagem_erro_xpath = '//*[@id="mensagem"]/p[1]'
        mensagem_erro = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, mensagem_erro_xpath))).text
        print(mensagem_erro)
        erro_especifico_xpath = '/html/body/div[7]/div[2]/form/div/div/div[3]/div/ul/li'
        erro_especifico = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, erro_especifico_xpath))).text
        if 'O valor do campo município não foi encontrado no sistema' in erro_especifico:
            cancelar_processo(driver)
       

    except Exception as e:
        print(f"Erro na correção do município: {e}")
        fechar_endereco_nota_XPATH = '/html/body/div[34]/div[1]/button'
        fechar_endereco_nota = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, fechar_endereco_nota_XPATH)))
        actions.move_to_element(fechar_endereco_nota).click().perform()
        salvar_alteracoes_nota(driver)


        return False  
'''
def verificar_erro_salvamento(driver):
    try:
        time.sleep(1)
        print("Verificando mensagem de erro após salvar a nota...")
        mensagem_erro_xpath = '//*[@id="mensagem"]/p[1]'
        mensagem_erro = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, mensagem_erro_xpath))).text
        print(mensagem_erro)
        erro_especifico_xpath = '/html/body/div[7]/div[2]/form/div/div/div[3]/div/ul/li'
        erro_especifico = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, erro_especifico_xpath))).text

        lista_erros.append(erro_especifico)
        
        if "Não foi possível salvar a Nota Fiscal" in mensagem_erro:
            print("Mensagem de erro detectada: Não foi possível salvar a Nota Fiscal")
            
            print(erro_especifico)
            
            '''  erros_municipio = ["O valor do campo município não foi encontrado no sistema", "UF válida"]
            if any(erro in erro_especifico for erro in erros_municipio):
                print('Erro específico no município encontrado.')
                #funcao_erro_municipio(driver)
                return False  
            
           '''
            print('Erro encontrado, mas não é específico do município.')
            return True
        
        
        print('Nenhuma mensagem de erro detectada após salvar a nota.')
        return False
        
    except Exception as e:
        print(f"Erro ao verificar mensagem de erro: {e}")#se der errado de verificara mensagem 
        return False

def cancelar_processo(driver):
    try:
        print("Cancelando processo")
        botao_cancelar_xpath = '/html/body/div[7]/div[2]/form/div/div/div[1]/div/div[2]/button'
        botao_cancelar = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, botao_cancelar_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_cancelar).click().perform()
        print("Processo cancelado.")
    except NoSuchElementException:
        print("Cancelando processo")
        botao_cancelar_xpath = '/html/body/div[8]/div[2]/form/div/div/div[1]/div/div[2]/button'
        botao_cancelar = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, botao_cancelar_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(botao_cancelar).click().perform()
        print("Processo cancelado.")
    except Exception as e:
        print(f"Erro ao cancelar o processo: {e}")

def existem_mais_notas_fiscais(driver, index):
    """
    Verifica se a nota fiscal na posição 'index' existe.
    Retorna True se a nota existir e False se não existir.
    """
    try:
        checkbox_xpath = f'/html/body/div[7]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div/input'
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
        return True
    except NoSuchElementException:
        checkbox_xpath = f'/html/body/div[8]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div/input'
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, checkbox_xpath))
        )
        print('estamos no cenário II de caminhos dos elementos')
        return True
    except:
        return False

def print_summary(success_count, error_count):
    print(f"Notas Fiscais emitidas com sucesso: {success_count}")
    print(f"Notas Fiscais com erros: {error_count}")

def main():
    driver = iniciar_driver()
    '''log_linhas= []
    def log_linhas(mensagem):
        if len(log_linhas) > 100:
            log_linhas.pop(0)'''

    if driver is not None:
        driver.get("https://www.bling.com.br/notas.fiscais.php#list")  # Abrir a página específica
        success_count = 0
        error_count = 0
        index = 1
        notas_inexistentes_consecutivas = 0  # Contador de notas inexistentes consecutivas

        while True:
            try:
                # Verificar se a nota existe
                if not existem_mais_notas_fiscais(driver, index):
                    notas_inexistentes_consecutivas += 1
                    print(f"Nota fiscal {index} não encontrada. Notas inexistentes consecutivas: {notas_inexistentes_consecutivas}")
                    
                    # Se duas notas consecutivas não existirem, encerrar o script
                    if notas_inexistentes_consecutivas >= 2:
                        print("Duas notas consecutivas não existem. Encerrando o script.")
                        break
                    
                    index += 1  # Tentar a próxima nota
                    continue
                
                # Se a nota for encontrada e processada, resetar o contador de notas inexistentes
                notas_inexistentes_consecutivas = 0
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
        print( lista_erros)
        driver.quit()
        '''for i in range(150):
                    log_linhas('imprimindo terminal teste {i}')
                    with open('ultimas_100_linhas_terminal.txt') as f:
                        for line in log_linhas:
                            f.write(line + '\n')'''
                    #print('ultimas 1000 linhas do log escritas noultimas_100_linhas_terminal.txt')

        #df = pd.DataFrame(lista_erros, success_count, error_count)
        #df.to_excel('rel_erros_SHP.xlsx', index=False)
    else:
        print("Não foi possível iniciar o driver.")

if __name__ == "__main__":
    main()