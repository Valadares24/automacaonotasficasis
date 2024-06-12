from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

service = Service('C:\\Users\\goias\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Abrir o Google
driver.get("https://www.google.com")

# Encontrar o campo de busca
search_box = driver.find_element(By.NAME, "q")

# Digitar "Selenium" no campo de busca e pressionar Enter
search_box.send_keys("Selenium")
search_box.send_keys(Keys.RETURN)

# Aguarde alguns segundos para que os resultados carreguem
driver.implicitly_wait(5)

# Pegar os títulos dos resultados da pesquisa
results = driver.find_elements(By.CSS_SELECTOR, 'h3')
for result in results:
    print(result.text)

# Fechar o navegador
driver.quit()