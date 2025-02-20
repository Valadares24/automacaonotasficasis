from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.common.keys import Keys
import time
import winsound 

# Função para iniciar o driver do Chrome
def iniciar_driver():
    try:    
        print("Iniciando o driver do Chrome...")    
        chrome_options = Options()
        # Corrigido para usar apenas o endereço de depuração
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
        driver = webdriver.Chrome(options=chrome_options)
        print("Driver iniciado com sucesso.")
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o driver do Chrome: {e}")
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        return None

def selecionar_checkbox_e_campo():
    global driver
    try:
        print("Tentando selecionar a primeira checkbox...")
        # Selecionar a primeira checkbox
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        print(f"Checkbox encontrada: {checkbox}")
        checkbox.click()
        print("Checkbox selecionada com sucesso.")
        
        # Esperar 2 segundos
        time.sleep(2)
        
        print("Tentando selecionar o campo associado à checkbox...")
        # Selecionar o campo associado à checkbox
        campo_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[3]/span[2]'
        campo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        print(f"Campo associado encontrado: {campo}")
        campo.click()
        print("Campo associado selecionado com sucesso.")
        
    except Exception as e:
        print(f"Erro ao selecionar a checkbox ou campo: {e}")

def processar_nota_fiscal():
    global driver
    try:
        selecionar_checkbox_e_campo()
        time.sleep(2)
        
        print("Iniciando a captura do CEP...")
        # BLOCO DE INTERAÇÃO COM CEP E DETERMINAÇÃO DE CFOP
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        cep_xpath = '/html/body/div[6]/div[2]/form/div/div/div[63]/div[3]/div/input'
        cep_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, cep_xpath))
        )
        time.sleep(2)
        cep_text = cep_field.get_attribute("value")
        cep_prefix = cep_text[:2]
        print(f"As duas primeiras casas do CEP são: {cep_prefix}")
        if cep_prefix.isdigit() and 72 <= int(cep_prefix) <= 76:
            cfop = 5102
        else:
            cfop = 6108
        print(f"Valor de CFOP determinado: {cfop}")
        time.sleep(2)
        
        print("Tentando selecionar e clicar no produto...")
        # Selecionar e clicar no produto em si
        novo_campo_xpath = '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[1]/td[9]/span[5]'
        print(f"XPath fornecido para o novo campo: {novo_campo_xpath}")
        
        def rolar_para_elemento(driver, xpath):
            print(f"Executando rolar_para_elemento com XPath: {xpath}") 
            try:
                elemento = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                print(f"Elemento com XPath {xpath} encontrado.")
                driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
                print(f"Página rolada até o elemento com XPath: {xpath}")
                is_displayed = elemento.is_displayed()
                print(f"Elemento visível: {is_displayed}")
            except Exception as e:
                winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
                print(f"Erro ao rolar para o elemento: {e}")
        
        def clicar_no_elemento(driver, xpath):
            print(f"Executando clicar_no_elemento com XPath: {xpath}")
            try:
                elemento = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                print(f"Elemento com XPath {xpath} está clicável.")
                time.sleep(2)
                driver.execute_script("arguments[0].click();", elemento)
                print(f"Elemento com XPath {xpath} clicado com JavaScript.")
            except Exception as e:
                winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
                print(f"Erro ao clicar no elemento com JavaScript: {e}")

        rolar_para_elemento(driver, novo_campo_xpath)
        time.sleep(2)
        clicar_no_elemento(driver, novo_campo_xpath)
        
        # COLAR NO CAMPO DESTINO($$$$MACROTAREFA$$$$$$$$$$)
        copiar_codigo_origem_xpath = '//*[@id="edCodigo"]'
        campo_origem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, copiar_codigo_origem_xpath))
        )
        print("Campo de origem encontrado.")

        if campo_origem.is_displayed():
            print("Campo de origem está visível.")
        else:
            print("Campo de origem não está visível.")
        
        # Copiar código do produto
        copiacodigo = campo_origem.get_attribute("value")
        if copiacodigo:
            print(f"Texto copiado: {copiacodigo}")
        else:
            print("Texto copiado está vazio ou None.")

        campo_destino_id = 'edDescricao'
        print(f"Tentando encontrar o elemento com ID: {campo_destino_id}")
        time.sleep(2)
        
        # Colar código do produto
        campo_destino = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, campo_destino_id))
        )
        print("Campo de destino encontrado.")
        driver.save_screenshot('campo_destino_encontrado.png')

        if campo_destino.is_displayed():
            print("Campo de destino está visível.")
        else:
            print("Campo de destino não está visível.")
            driver.save_screenshot('campo_destino_nao_visivel.png')

        time.sleep(2)

        try:
            print("Tentando limpar o campo de destino.")
            campo_destino.clear()
            print("Campo de destino limpo. Tentando colar o texto.")
            campo_destino.send_keys(copiacodigo)
            print(f"Texto colado no elemento com ID {campo_destino_id}: {copiacodigo}")
            driver.save_screenshot('texto_colado.png')
        except Exception as e:
            print(f"Erro ao colar o texto no campo de destino: {e}")
            winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
            driver.save_screenshot('erro_colar_texto.png')

        # Abrindo produto - seta pra baixo
        time.sleep(2)
        try:
            print("Tentando pressionar a seta para baixo.")
            campo_destino.send_keys(Keys.ARROW_DOWN)
            print("Seta para baixo pressionada com sucesso.")
            driver.save_screenshot('pressionar_seta_para_baixo.png')
        except Exception as e:
            print(f"Erro ao pressionar a seta para baixo: {e}")
            winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
            driver.save_screenshot('erro_pressionar_seta_para_baixo.png')

        time.sleep(2)
        
        # Clicando no produto
        campo_produto_xpath = '/html/body/ul[3]/li/a'
        try:
            print(f"Tentando encontrar o elemento com XPath: {campo_produto_xpath}")
            campo_produto = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, campo_produto_xpath))
            )
            print("Campo de texto 'produto' encontrado.")
            driver.save_screenshot('campo_produto_encontrado.png')
            campo_produto.click()
            print(f"Campo de texto 'produto' com XPath {campo_produto_xpath} clicado.")
            driver.save_screenshot('campo_produto_clicado.png')
        except Exception as e:
            print(f"Erro ao clicar no campo de texto 'produto': {e}")
            winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        
        print("Tentando colar o valor no campo CFOP...")
        # Achar CFOP e colar valor
        campo_cfop_xpath = '/html/body/div[28]/form/div/div/div/div[3]/div[9]/input'
        try:
            print(f"Tentando encontrar o elemento com XPath: {campo_cfop_xpath}")
            campo_cfop = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, campo_cfop_xpath))
            )
            print("Campo CFOP encontrado.")
            driver.save_screenshot('campo_cfop_encontrado.png')
            time.sleep(2)
            print(f"Colando o valor {cfop} no campo CFOP.")
            campo_cfop.clear()
            campo_cfop.send_keys(str(cfop))
            print(f"Valor {cfop} colado no campo CFOP.")
            driver.save_screenshot('valor_cfop_colado.png')                     
        except Exception as e:
            print(f"Erro ao colar o valor no campo CFOP: {e}")
            winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
            time.sleep(2)
        
        # Salvar alterações no item da nota
        try:
            print("Tentando salvar as alterações no item da nota...")
            botao_salvar_item_xpath = '/html/body/div[28]/div[2]/div/button'  # Preencha o XPath do botão de salvar alterações
            botao_salvar_item = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
            )
            botao_salvar_item.click()
            print("Alterações no item da nota salvas com sucesso.")
            time.sleep(2)
        except Exception as e:
            winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
            print(f"Erro ao salvar as alterações no item da nota: {e}")

    #   Clicando no produto novamente
        clicar_no_elemento(driver, novo_campo_xpath)
        ####trecho de apagar desconto do item
        print("Tentando apagar o valor do desconto...")
        # Apagando desconto
        campo_apagar_xpath = '//*[@id="edValorDescontoItem"]'
        time.sleep(2)
        try:
            print(f"Tentando encontrar o campo com XPath: {campo_apagar_xpath}")
            campo_apagar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, campo_apagar_xpath))
            )
            print("Campo de desconto encontrado.")
            campo_apagar.clear()
            print("Desconto apagado.")
        except Exception as e:
            winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
            print(f"Erro ao apagar o desconto: {e}")
        
        print("Processo concluído.")
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"Ocorreu um erro inesperado: {e}")
        ####trecho de apagar desconto do item

    # Salvar alterações no item da nota
    try:
        print("Tentando salvar as alterações no item da nota...")
        botao_salvar_item_xpath = '/html/body/div[28]/div[2]/div/button'  # Preencha o XPath do botão de salvar alterações
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(2)
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"Erro ao salvar as alterações no item da nota: {e}")

# Salvar alterações no item da nota
    try:
        print("Tentando salvar as alterações no item da nota...")
        botao_salvar_item_xpath = '/html/body/div[28]/div[2]/div/button'  # Preencha o XPath do botão de salvar alterações
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("Alterações no item da nota salvas com sucesso.")
        time.sleep(2)
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"Erro ao salvar as alterações no item da nota: {e}")

        # Salvar alterações DA NOTA
    try:
        print("Tentando salvar as alterações na nota...")
        botao_salvar_item_xpath = '//*[@id="botaoSalvar"]'  # Preencha o XPath do botão de salvar alterações
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("Alterações na nota salvas com sucesso.")
        time.sleep(2)
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"Erro ao salvar as alterações na nota: {e}")

        time.sleep(5)
        #adicionar condicional de erro neste ponto
        
    # EVNIAR A NOTA
    try:
        print("Tentando enviar a nota salva")
        botao_salvar_item_xpath = '//*[@id="container"]/div[3]/div[2]/div/div[1]/button[1]/span[2]'  # Preencha o XPath do botão de salvar alterações
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("Alterações na nota salvas com sucesso.")
        time.sleep(2)
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"Erro ao enviar a nota: {e}")
        
        time.sleep(2)
        # EVNIAR A NOTA #2
    try:
        print("Tentando enviar a nota salva")
        botao_salvar_item_xpath = '//*[@id="notaAcao"]'  # Preencha o XPath do botão de salvar alterações
        botao_salvar_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("nota enviada")
        time.sleep(2)
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"Erro ao enviar a nota: {e}")
        
         
    # VALIDAR ENVIO - FINAL
    try:
        print("Validar envio da nota salva")
        time.sleep(25)
        botao_salvar_item_xpath = '//*[@id="notaAcao"]'  # Preencha o XPath do botão de salvar alterações
        botao_salvar_item = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, botao_salvar_item_xpath))
        )
        botao_salvar_item.click()
        print("envio validado")
        time.sleep(2)
    except Exception as e:
        winsound.Beep(1000, 2000)  # 1000 Hz por 500 milissegundos
        print(f"erro ao valiodar envio {e}")


def existem_mais_notas_fiscais(driver):
    try:
        # Verifica se há mais checkboxes na página
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, checkbox_xpath))
        )
        return True  # Retorna True se encontrar a checkbox
    except:
        return False  # Retorna False se não encontrar a checkbox

# Função principal
def main():
    global driver
    print("Executando a função principal...")
    driver = iniciar_driver()
    if driver is not None:
        while existem_mais_notas_fiscais(driver):  # Loop para processar todas as notas fiscais
            processar_nota_fiscal()
        driver.quit()
        print("Driver encerrado.")
    else:
        print("Não foi possível iniciar o driver.")

if __name__ == "__main__":
    main()
