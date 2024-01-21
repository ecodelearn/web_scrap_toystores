import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para coletar informações de um nível (produto) e salvar em um CSV
def collect_level_data_and_save(level_element, product_index):
    # Rola a página para que o elemento seja visível
    scroll_to_element(level_element)

    # Aguarde até que o elemento seja clicável
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, level_xpath)))
    except TimeoutError:
        print("Elemento não clicável.")
        return

    level_element.click()

    # Aguarde até que a página do nível (produto) seja carregada (ajuste o tempo limite conforme necessário)
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="product-name"]')))
    except TimeoutError:
        print("Elemento de título do produto não encontrado.")
        return

    try:
        # Encontre o nome do produto usando o XPath fornecido
        title_element = driver.find_element(By.XPATH, '//*[@id="product-name"]')
        product_name = title_element.text

        # Encontre o preço do produto usando o XPath fornecido
        price_element = driver.find_element(By.XPATH, '//*[@id="price_display"]')
        price = price_element.text

        # Encontre a descrição do produto usando o XPath fornecido
        description_element = driver.find_element(By.XPATH, '/html/body/div[10]/div/div[1]/div[2]/div[7]')
        description = description_element.text

        # Salve os dados em um arquivo CSV com base no índice do produto
        csv_filename = f'produto_{product_index}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Nome do Produto', 'Preço', 'Descrição']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Nome do Produto': product_name, 'Preço': price, 'Descrição': description})

    except NoSuchElementException:
        print("Informações do nível (produto) não encontradas.")

    # Volte para a página principal
    driver.get('https://plantandoebrincando.com.br/produtos/?mpage=100')
    # Aguarde 2 segundos para evitar problemas de carregamento
    time.sleep(2)

# Função para rolar a página em 10 passos
def scroll_to_element(element):
    for _ in range(10):
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
        time.sleep(1)  # Aguarde 1 segundo entre as rolagens

# Inicialize o driver
driver = webdriver.Chrome()
driver.get('https://plantandoebrincando.com.br/produtos/?mpage=100')

# Aguarde 10 segundos
time.sleep(10)

# Loop através dos níveis (produtos)
for i in range(1, 1000):  # Supondo que existem 100 produtos na página
    level_xpath = f'/html/body/section[2]/div/div/div[2]/div[3]/div[{i}]/div/a'
    level_element = driver.find_element(By.XPATH, level_xpath)

    # Chame a função para coletar informações e salvar em um CSV
    collect_level_data_and_save(level_element, i)

# Feche o driver
driver.quit()