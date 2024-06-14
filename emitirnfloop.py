from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Função para iniciar o driver do Chrome
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


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

def processar_nota_fiscal():
    try:
        selecionar_checkbox_e_campo()
        time.sleep(2)
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
        print("Valor de cfop:", cfop)
        time.sleep(2)
        
        # Selecionar e clicar no produto
        novo_campo_xpath = '/html/body/div[6]/div[2]/form/div/div/div[42]/table/tbody/tr[1]/td[1]'
        print(f"XPath fornecido para o novo campo: {novo_campo_xpath}")
#rolar para elemento
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
                print(f"Erro ao rolar para o elemento: {e}")
#clicar produto
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
                print(f"Erro ao clicar no elemento com JavaScript: {e}")

        rolar_para_elemento(driver, novo_campo_xpath)
        time.sleep(2)
        clicar_no_elemento(driver, novo_campo_xpath)

        # COLAR NO CAMPO DESTINO(MACROTAREFA)
        campo_origem_xpath = '/html/body/div[28]/form/div/div/div/div[1]/div[2]/input'
        campo_origem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, campo_origem_xpath))
        )
        print("Campo de origem encontrado.")

        if campo_origem.is_displayed():
            print("Campo de origem está visível.")
        else:
            print("Campo de origem não está visível.")
#copiar codigo produto
        copiacodigo = campo_origem.get_attribute("value")
        if copiacodigo:
            print(f"Texto copiado: {copiacodigo}")
        else:
            print("Texto copiado está vazio ou None.")

        campo_destino_id = 'edDescricao'
        print(f"Tentando encontrar o elemento com ID: {campo_destino_id}")
        time.sleep(2)
#colar codigo produto
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
            driver.save_screenshot('erro_colar_texto.png')

#abrindo produto - seta pra baixo
        time.sleep(2)
        try:
            print("Tentando pressionar a seta para baixo.")
            campo_destino.send_keys(Keys.ARROW_DOWN)
            print("Seta para baixo pressionada com sucesso.")
            driver.save_screenshot('pressionar_seta_para_baixo.png')
        except Exception as e:
            print(f"Erro ao pressionar a seta para baixo: {e}")
            driver.save_screenshot('erro_pressionar_seta_para_baixo.png')

        time.sleep(2)
#clicando no produto
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
            driver.save_screenshot('erro_clicar_produto.png')
#achar cfop e colar valor
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
            driver.save_screenshot('erro_campo_cfop.png')
            time.sleep(2)
#apagando desconto
        campo_apagar_id = 'desconto'
        try:
            print(f"Tentando encontrar o campo com XPath: {campo_apagar_id}")
            campo_apagar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, campo_apagar_id))
            )
            print("Campo encontrado.")

            if campo_apagar.is_displayed():
                print("Campo está visível.")
            else:
                print("Campo não está visível.")

            print("Tentando apagar o valor do campo.")
            campo_apagar.clear()
            print("Valor do campo apagado.")
        except Exception as e:
            print(f"Erro ao apagar o valor do campo: {e}")
#salvar nota.pt1
        botao_salvar_xpath = '/html/body/div[27]/div[2]/div/button'
        time.sleep(1)
        try:
            print(f"Tentando encontrar o botão de salvar com XPath: {botao_salvar_xpath}")
            botao_salvar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, botao_salvar_xpath))
            )
            print("Botão de salvar encontrado.")
            botao_salvar.click()
            print("Botão de salvar clicado.")
        except Exception as e:
            print(f"Erro ao clicar no botão de salvar: {e}")
            time.sleep(1)
#salvar nota.pt2
        outro_botao_salvar_xpath = '/html/body/div[6]/div[2]/form/div/div/div[1]/div/div[3]/button'
        time.sleep(1)
        try:
            print(f"Tentando encontrar o outro botão de salvar com XPath: {outro_botao_salvar_xpath}")
            outro_botao_salvar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, outro_botao_salvar_xpath))
            )
            print("Outro botão de salvar encontrado.")
            time.sleep(1)
            outro_botao_salvar.click()
            print("Outro botão de salvar clicado.")
        except Exception as e:
            print(f"Erro ao clicar no outro botão de salvar: {e}")
#clicando no emitir nota
        campo_emissao_notas_xpath = '/html/body/div[6]/div[8]/div[3]/div[2]/div/div[1]/button[1]/span[2]'
        try:
            print(f"Tentando encontrar o campo de emissão de notas com XPath: {campo_emissao_notas_xpath}")
            campo_emissao_notas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, campo_emissao_notas_xpath))
            )
            print("Campo de emissão de notas encontrado.")
            campo_emissao_notas.click()
            print("Campo de emissão de notas clicado.")
        except Exception as e:
            print(f"Erro ao clicar no campo de emissão de notas: {e}")
#enviar nota
        campo_enviar_notas_xpath = '/html/body/div[27]/div[3]/div/button'
        try:
            print(f"Tentando encontrar o campo de envio de notas com XPath: {campo_enviar_notas_xpath}")
            campo_enviar_notas = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, campo_enviar_notas_xpath))
            )
            print("Campo de enviar de notas encontrado.")
            campo_enviar_notas.click()
            print("Campo de enviar de notas clicado.")
        except Exception as e:
            print(f"Erro ao clicar no campo de enviar de notas: {e}")
        time.sleep(18)
#sair da nota
        campo_fechar_notas_xpath = '/html/body/div[27]/div[3]/div/button'
        try:
            print(f"Tentando encontrar o campo de fechamento de notas com XPath: {campo_fechar_notas_xpath}")
            campo_fechar_notas = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, campo_fechar_notas_xpath))
            )
            print("Campo de fechamento de notas encontrado.")
            campo_fechar_notas.click()
            print("Campo de fechamento de notas clicado.")
        except Exception as e:
            print(f"Erro ao clicar no campo de fechamento de notas: {e}")

        return True

    except Exception as e:
        print(f"Erro ao processar a nota fiscal: {e}")
        return False
#repetir processo-loop
def existem_mais_notas_fiscais(driver):
    try:
        elemento = driver.find_element(By.XPATH, "/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label")
        return elemento is not None
    except:
        return False

if __name__ == "__main__":
    driver = iniciar_driver()
    while existem_mais_notas_fiscais(driver):
        if not processar_nota_fiscal():
            break
        time.sleep(2)  # Delay entre cada iteração do loop

    print("Todas as notas fiscais foram processadas.")
    driver.quit()
