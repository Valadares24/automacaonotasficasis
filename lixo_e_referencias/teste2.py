from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def iniciar_driver():
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o driver do Chrome: {e}")
        return None

def main():
    driver = iniciar_driver()
    if driver:
        driver.get("http://www.google.com")
        print(driver.title)
        driver.quit()
    else:
        print("Não foi possível iniciar o driver.")

if __name__ == "__main__":
    main()
