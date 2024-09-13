from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def iniciar_driver():
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        print("Driver iniciado com sucesso.")
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o driver do Chrome: {e}")
        return None
#inicia normalmente
def verificar_status_nota(driver, index):
    """ Verifica o status da nota fiscal e retorna True se for 'Pendente'. """
    situacao_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[5]/span[2]/span'
    try:
        situacao_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, situacao_xpath))
        )
        situacao_texto = situacao_element.text
        return 'Pendente' in situacao_texto
    except Exception as e:
        print(f"Erro ao verificar status da nota: {e}")
        return False

def processar_nota_fiscal(driver, index):
    if verificar_status_nota(driver, index):
        print(f"Processando nota fiscal no índice {index}...")
        # Aqui você coloca o código para processar a nota
    else:
        print(f"Nota no índice {index} não está pendente e será pulada.")

def main():
    driver = iniciar_driver()
    if driver:
        driver.get("https://www.bling.com.br/notas.fiscais.php#list")
        index = 1
        while existem_mais_notas_fiscais(driver, index):
            processar_nota_fiscal(driver, index)
            index += 1
        driver.quit()

def existem_mais_notas_fiscais(driver, index):
    try:
        checkbox_xpath = f'/html/body/div[6]/div[8]/div[2]/div[7]/table/tbody/tr[{index}]/td[1]/div/label'
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, checkbox_xpath))
        )
        return True
    except:
        return False

if __name__ == "__main__":
    main()
