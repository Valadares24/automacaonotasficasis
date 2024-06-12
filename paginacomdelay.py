from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_dynamic_element_by_xpath(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return element
    except:
        print(f"Elemento com XPath {xpath} não encontrado.")
        return None

""" def get_element_by_id(driver, element_id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        return element
    except:
        print(f"Elemento com ID {element_id} não encontrado.")
        return None

def get_element_by_class(driver, class_name):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        )
        return element
    except:
        print(f"Elemento com a classe {class_name} não encontrado.")
        return None
     """
    

# Configurar opções do Chrome para depuração remota
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Inicializar o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# Certificar-se de que o Selenium está controlando a janela correta
driver.switch_to.window(driver.window_handles[0])

# Verificar a URL da página
current_url = driver.current_url
print(f"URL atual: {current_url}")

expected_url = "https://www.bling.com.br/notas.fiscais.php#list"
if current_url != expected_url:
    print("Você não está na página esperada. Verifique a URL e tente novamente.")
else:
    print("Você está na página correta.")

    # Esperar que a página carregue (se necessário)
    time.sleep(5)

    # Selecionar o checkbox dinamicamente pelo XPath
    checkbox_xpath = "//input[contains(@id, marcadodatatable20480115941)]"
    checkbox = get_dynamic_element_by_xpath(driver, checkbox_xpath)
    if checkbox:
        if not checkbox.is_selected():
            checkbox.click()
        print("Checkbox selecionado.")
        time.sleep(2)  # Aguardar para ver a interação

    # Selecionar o campo com a classe 'title-form' dinamicamente pelo XPath
    title_form_xpath = "//div[contains(@class, @value = 'visible-xs table-label')]"
    title_form_field = get_dynamic_element_by_xpath(driver, title_form_xpath)
    if title_form_field:
        title_form_field.click()
        print("Campo 'title-form' selecionado.")
        time.sleep(2)  # Aguardar para ver a interação


# Fechar o navegador após a interação (opcional)
# driver.quit()
