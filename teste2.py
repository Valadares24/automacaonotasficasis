# Importa as bibliotecas necessárias
from selenium import webdriver  # Importa o WebDriver do Selenium
from selenium.webdriver.common.by import By  # Importa a classe By para selecionar elementos
from selenium.webdriver.common.keys import Keys  # Importa a classe Keys para simular pressionamento de teclas
import time  # Importa a biblioteca time para pausas no código
from selenium.webdriver.chrome.service import Service

# Configurações do navegador
options = webdriver.ChromeOptions()  # Cria um objeto de opções para o Chrome
options.add_argument('--headless')  # Adiciona o argumento para rodar o Chrome em modo headless (sem interface gráfica)
options.add_argument('--no-sandbox')  # Adiciona o argumento para desabilitar o sandboxing
options.add_argument('--disable-dev-shm-usage')  # Adiciona o argumento para desabilitar o uso compartilhado de memória

service = Service('C:\\Users\\goias\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

print("WebDriver inicializado com sucesso.")

# URL do sistema de emissão de notas fiscais
url = 'https://www.bling.com.br/notas.fiscais.php#list'

# Informações de login
username = 'financeiro@goiaspet.com.br'
password = 'Goiaspet2022*'

# Função para realizar login
def login(username, password):
    driver.get(url)  # Abre a URL fornecida no navegador
    time.sleep(3)  # Espera 3 segundos para garantir que a página carregue completamente
    driver.find_element(By.ID, 'username').send_keys(username)  # Encontra o campo de usuário pelo ID e insere o nome de usuário
    driver.find_element(By.ID, 'password').send_keys(password)  # Encontra o campo de senha pelo ID e insere a senha
    driver.find_element(By.CLASS_NAME, 'login-button').click()  # Encontra o botão de login pela classe e clica nele
    time.sleep(3)  # Espera 3 segundos para garantir que o login seja processado

# Executa o login
login(username, password)  # Chama a função de login com o nome de usuário e senha fornecidos

# Função para emitir nota fiscal
def emitir_nota():
    # Seleciona o checkbox do item de NF
    driver.find_element(By.CLASS_NAME, 'checkbox-item').click()  # Encontra o checkbox pelo nome da classe e clica nele
    time.sleep(2)  # Espera 2 segundos

    # Abre a nota fiscal
    driver.find_element(By.ID, 'item0').click()  # Encontra o item de nota fiscal pelo ID e clica nele
    time.sleep(2)  # Espera 2 segundos

    # Rola a tela para baixo e abre o campo UF
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")  # Executa um script JavaScript para rolar a página para baixo
    time.sleep(2)  # Espera 2 segundos
    
    uf_select = Select(driver.find_element(By.NAME, 'uf'))  # Encontra o campo de seleção de UF pelo nome e cria um objeto Select
    uf_select.select_by_value('62')  # Seleciona o valor '62' no campo de seleção
    time.sleep(2)  # Espera 2 segundos

    # Define o código CFOP com base no código UF
    cfop_code = '5102' if uf_select.first_selected_option.get_attribute('value') == '62' else '6108'  # Define o código CFOP com base no valor selecionado

    # Fecha o campo UF
    driver.find_element(By.NAME, 'uf').send_keys(Keys.ESCAPE)  # Envia a tecla ESCAPE para fechar o campo de seleção de UF
    time.sleep(2)  # Espera 2 segundos

    # Rola a tela para baixo e abre o campo para copiar o código do produto
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Executa um script JavaScript para rolar a página para baixo
    time.sleep(2)  # Espera 2 segundos

    # Copia o código do produto
    codigo_produto = driver.find_element(By.NAME, 'edCodigo').get_attribute('value')  # Encontra o campo de código do produto pelo nome e obtém seu valor
    
    # Cola o código do produto no campo de nome do produto
    driver.find_element(By.NAME, 'edDescricao').send_keys(codigo_produto)  # Encontra o campo de descrição pelo nome e insere o código do produto
    time.sleep(2)  # Espera 2 segundos

    # Cola o código CFOP
    driver.find_element(By.NAME, 'edCfop').send_keys(cfop_code)  # Encontra o campo de CFOP pelo nome e insere o código CFOP
    time.sleep(2)  # Espera 2 segundos

    # Salva a nota
    driver.find_element(By.CLASS_NAME, 'Button--primary').click()  # Encontra o botão de salvar pela classe e clica nele
    time.sleep(2)  # Espera 2 segundos

    # Salva externamente
    driver.find_element(By.ID, 'botaoSalvar').click()  # Encontra o botão de salvar externo pelo ID e clica nele
    time.sleep(2)  # Espera 2 segundos

# Executa a emissão da nota fiscal
emitir_nota()  # Chama a função de emitir nota fiscal


# Fecha o navegador
driver.quit()  # Fecha o navegador e encerra a sessão do WebDriver
