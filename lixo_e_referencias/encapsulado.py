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
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
        driver = webdriver.Chrome(options=chrome_options)
        print('driver iniciado')
        return driver
    except Exception as e:
        print(f'erro iniciando driver: {e}')
        return None
    
