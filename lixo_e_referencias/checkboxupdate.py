from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Configurar opções do Chrome para depuração remota
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Inicializar o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Capturar o ID da aba aberta
current_window_handle = driver.current_window_handle
print("FB080D63CD8AB09BD0D57C7B8589B38E", current_window_handle)

# Lista de todas as abas abertas
window_handles = driver.window_handles
print("FB080D63CD8AB09BD0D57C7B8589B38E", window_handles)

# Certifique-se de que você está na página correta
expected_url = "https://www.bling.com.br/notas.fiscais.php#list"
if driver.current_url != expected_url:
    print("Você não está na página esperada. Verifique a URL e tente novamente.")
    driver.quit()
    exit()

# Esperar que a página carregue (se necessário)
time.sleep(2)

# Função para selecionar a checkbox e o campo associado
def selecionar_checkbox_e_campo():
    try:
        # Selecionar a primeira checkbox
        checkbox_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[1]/div/label'
        checkbox = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
        )
        checkbox.click()
        print("Checkbox selecionada.")
        
        # Esperar 2 segundos
        time.sleep(2)
        
        # Selecionar o campo associado à checkbox
        campo_xpath = '/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[1]/td[3]/span[2]'
        campo = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, campo_xpath))
        )
        campo.click()
        print("Campo associado selecionado.")
        
    except Exception as e:
        print(f"Erro ao selecionar a checkbox ou campo: {e}")

# Executa a função para selecionar a checkbox e o campo associado
selecionar_checkbox_e_campo()

time.sleep(2)
######### BLOCO DE INTERAÇÃO COM CEP E DETERMINAÇÃO DE CFOP #######################################################
# Rolar a página para baixo
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Forneça o XPath para o campo "cep"
cep_xpath = '/html/body/div[6]/div[2]/form/div/div/div[63]/div[3]/div/input'  # Substitua pelo XPath do campo "cep"

# Selecionar o campo com XPath fornecido
cep_field = WebDriverWait(driver, 6).until(
    EC.presence_of_element_located((By.XPATH, cep_xpath))
)

# Esperar 2 segundos
time.sleep(2)

# Selecionar o campo com a classe 'title-form'
title_form_field = WebDriverWait(driver, 6).until(
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
    print(f"Executando rolar_para_elemento com XPath: {xpath}")
    try:
        # Esperar que o elemento esteja presente na página
        elemento = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        print(f"Elemento com XPath {xpath} encontrado.")

        # Rolar a página até o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        print(f"Página rolada até o elemento com XPath: {xpath}")

        # Verificar se o elemento está visível
        is_displayed = elemento.is_displayed()
        print(f"Elemento visível: {is_displayed}")
    except Exception as e:
        print(f"Erro ao rolar para o elemento: {e}")

# Função para clicar no elemento especificado pelo XPath
def clicar_no_elemento(driver, xpath):
    print(f"Executando clicar_no_elemento com XPath: {xpath}")
    try:
        # Esperar que o elemento esteja presente e clicável na página
        elemento = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"Elemento com XPath {xpath} está clicável.")
        time.sleep(2)
        # Usar JavaScript para clicar no elemento
        driver.execute_script("arguments[0].click();", elemento)
        print(f"Elemento com XPath {xpath} clicado com JavaScript.")
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

#############COLAR NO CAMPO DESTINO
try:
    # Localizar o campo de origem (onde o texto será copiado)
    campo_origem_xpath = '/html/body/div[27]/form/div/div/div/div[1]/div[2]/input'
    campo_origem = WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, campo_origem_xpath))
    )
    print("Campo de origem encontrado.")

    # Verificar se o campo de origem está visível
    if campo_origem.is_displayed():
        print("Campo de origem está visível.")
    else:
        print("Campo de origem não está visível.")

    # Copiar o texto do campo de origem e armazenar na variável copiacodigo
    copiacodigo = campo_origem.get_attribute("value")
    if copiacodigo:
        print(f"Texto copiado: {copiacodigo}")
    else:
        print("Texto copiado está vazio ou None.")
    
    # Localizar o campo de destino pelo ID
    campo_destino_id = 'edDescricao'
    print(f"Tentando encontrar o elemento com ID: {campo_destino_id}")
    time.sleep(2)

    campo_destino = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, campo_destino_id))
    )
    print("Campo de destino encontrado.")
    driver.save_screenshot('campo_destino_encontrado.png')

    # Verificar se o campo de destino está visível
    if campo_destino.is_displayed():
        print("Campo de destino está visível.")
    else:
        print("Campo de destino não está visível.")
        driver.save_screenshot('campo_destino_nao_visivel.png')

    # Tentar colar o texto no campo de destino
    time.sleep(2)

    try:
        print("Tentando limpar o campo de destino.")
        campo_destino.clear()  # Limpar o campo antes de colar o texto, se necessário
        print("Campo de destino limpo. Tentando colar o texto.")
        campo_destino.send_keys(copiacodigo)
        print(f"Texto colado no elemento com ID {campo_destino_id}: {copiacodigo}")
        driver.save_screenshot('texto_colado.png')
    except Exception as e:
        print(f"Erro ao colar o texto no campo de destino: {e}")
        driver.save_screenshot('erro_colar_texto.png')

    # Pressionar a seta para baixo no teclado
    try:
        print("Tentando pressionar a seta para baixo.")
        campo_destino.send_keys(Keys.ARROW_DOWN)
        print("Seta para baixo pressionada com sucesso.")
        driver.save_screenshot('pressionar_seta_para_baixo.png')
    except Exception as e:
        print(f"Erro ao pressionar a seta para baixo: {e}")
        driver.save_screenshot('erro_pressionar_seta_para_baixo.png')
        
    time.sleep(2)

    # Localizar o campo de texto 'produto' pelo XPath e clicar nele
    campo_produto_xpath = '/html/body/ul[3]/li/a'
    try:
        print(f"Tentando encontrar o elemento com XPath: {campo_produto_xpath}")
        campo_produto = WebDriverWait(driver, 6).until(
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

except Exception as e:
    print(f"Erro ao localizar elemento ou colar texto: {e}")
    driver.save_screenshot('erro.png')

print("Aguardando novas instruções ou ações manuais...")
###########################################################################################
# Selecionar o campo com o XPath fornecido e colar o valor da variável cfop
campo_cfop_xpath = '/html/body/div[27]/form/div/div/div/div[3]/div[9]/input'
try:
    print(f"Tentando encontrar o elemento com XPath: {campo_cfop_xpath}")
    campo_cfop = WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, campo_cfop_xpath))
    )
    print("Campo CFOP encontrado.")
    driver.save_screenshot('campo_cfop_encontrado.png')
    time.sleep(2)
    # Colar o valor da variável cfop no campo CFOP
    print(f"Colando o valor {cfop} no campo CFOP.")
    campo_cfop.clear()  # Limpar o campo antes de colar o texto, se necessário
    campo_cfop.send_keys(str(cfop))
    print(f"Valor {cfop} colado no campo CFOP.")
    driver.save_screenshot('valor_cfop_colado.png')
except Exception as e:
    print(f"Erro ao colar o valor no campo CFOP: {e}")
    driver.save_screenshot('erro_campo_cfop.png')
    time.sleep(2)

# Selecionar o campo e apagar o valor que há escrito nele
campo_apagar_xpath = '/html/body/div[27]/form/div/div/div/div[3]/div[6]/input'
try:
    print(f"Tentando encontrar o campo com XPath: {campo_apagar_xpath}")
    campo_apagar = WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, campo_apagar_xpath))
    )
    print("Campo encontrado.")

    # Verificar se o campo está visível
    if campo_apagar.is_displayed():
        print("Campo está visível.")
    else:
        print("Campo não está visível.")

    # Apagar o valor do campo
    print("Tentando apagar o valor do campo.")
    campo_apagar.clear()  # Limpar o campo para deixá-lo completamente em branco
    print("Valor do campo apagado.")
except Exception as e:
    print(f"Erro ao apagar o valor do campo: {e}")


# Selecionar o botão de salvar a nota e clicar nele
botao_salvar_xpath = '/html/body/div[27]/div[2]/div/button'
time.sleep(1)
try:
    print(f"Tentando encontrar o botão de salvar com XPath: {botao_salvar_xpath}")
    botao_salvar = WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable((By.XPATH, botao_salvar_xpath))
    )
    print("Botão de salvar encontrado.")

    # Clicar no botão de salvar
    botao_salvar.click()
    print("Botão de salvar clicado.")
except Exception as e:
    print(f"Erro ao clicar no botão de salvar: {e}")
    time.sleep(1)

# Selecionar o outro botão de salvar a nota e clicar nele
outro_botao_salvar_xpath = '/html/body/div[6]/div[2]/form/div/div/div[1]/div/div[3]/button'
time.sleep(1)
try:
    print(f"Tentando encontrar o outro botão de salvar com XPath: {outro_botao_salvar_xpath}")
    outro_botao_salvar = WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable((By.XPATH, outro_botao_salvar_xpath))
    )
    print("Outro botão de salvar encontrado.")
    time.sleep(1)
    # Clicar no outro botão de salvar
    outro_botao_salvar.click()
    print("Outro botão de salvar clicado.")
except Exception as e:
    print(f"Erro ao clicar no outro botão de salvar: {e}")

# Selecionar o campo de emissão de notas e clicar nele
campo_emissao_notas_xpath = '/html/body/div[6]/div[8]/div[3]/div[2]/div/div[1]/button[1]/span[2]'
try:
    print(f"Tentando encontrar o campo de emissão de notas com XPath: {campo_emissao_notas_xpath}")
    campo_emissao_notas = WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable((By.XPATH, campo_emissao_notas_xpath))
    )
    print("Campo de emissão de notas encontrado.")

    # Clicar no campo de emissão de notas
    campo_emissao_notas.click()
    print("Campo de emissão de notas clicado.")
except Exception as e:
    print(f"Erro ao clicar no campo de emissão de notas: {e}")

# Selecionar o campo de enviar de notas e clicar nele
campo_enviar_notas_xpath = '/html/body/div[27]/div[3]/div/button'
try:
    print(f"Tentando encontrar o campo de emissão de notas com XPath: {campo_enviar_notas_xpath}")
    campo_enviar_notas = WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable((By.XPATH, campo_enviar_notas_xpath))
    )
    print("Campo de enviar de notas encontrado.")

    # Clicar no campo de enviar de notas
    campo_enviar_notas.click()
    print("Campo de enviar de notas clicado.")
except Exception as e:
    print(f"Erro ao clicar no campo de enviar de notas: {e}")
time.sleep(12)

# Selecionar o campo de fechar de notas e clicar nele
campo_fechar_notas_xpath = '/html/body/div[27]/div[3]/div/button'
try:
    print(f"Tentando encontrar o campo de emissão de notas com XPath: {campo_fechar_notas_xpath}")
    campo_fechar_notas = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, campo_fechar_notas_xpath))
    )
    print("Campo de fechamento de notas encontrado.")

    # Clicar no campo de fechamento de notas
    campo_fechar_notas.click()
    print("Campo de fechamento de notas clicado.")
except Exception as e:
    print(f"Erro ao clicar no campo de fechamento de notas: {e}")


print("Aguardando novas instruções ou ações manuais...")
# Aguarda indefinidamente para permitir interação manual ou futuras instruções
while True:
    time.sleep(1)
# Aguarda indefinidamente para permitir interação manual ou futuras instruções
while True:
    time.sleep(1)
