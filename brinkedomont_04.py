import os
import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicialize o driver do Chrome
driver = webdriver.Chrome()

# Função para coletar informações de um produto e salvar em um CSV
def collect_product_data_and_save(page_number, product_index):
    # Crie um diretório para a página atual, se ainda não existir
    page_directory = f'pagina{page_number}'
    if not os.path.exists(page_directory):
        os.makedirs(page_directory)

    # Encontre todos os links com a classe "item-link"
    product_links = driver.find_elements(By.CLASS_NAME, 'item-link')

    if len(product_links) >= product_index:
        # Obtenha o link do produto com base no índice
        product_link = product_links[product_index - 1].get_attribute('href')

        # Verifique se o link do produto é válido
        if product_link:
            # Abra a página do produto
            driver.get(product_link)

            # Aguarde até que a página do produto seja carregada (ajuste o tempo limite conforme necessário)
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'js-product-name')))
            except TimeoutError:
                print(f"Elemento de nome do produto {product_index} na página {page_number} não encontrado.")
                return

            # Colete os dados do produto
            try:
                product_name_element = driver.find_element(By.CLASS_NAME, 'js-product-name')
                product_name = product_name_element.text

                price_element = driver.find_element(By.ID, 'price_display')
                price = price_element.text

                description_element = driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/div[1]/div[1]')
                description = description_element.text

                # Salve os dados em um arquivo CSV no diretório correspondente
                csv_filename = os.path.join(page_directory, f'produto_{product_index}.csv')
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Nome do Produto', 'Preço', 'Descrição']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'Nome do Produto': product_name, 'Preço': price, 'Descrição': description})

            except NoSuchElementException:
                print(f"Informações do produto {product_index} na página {page_number} não encontradas.")

            # Volte para a página inicial
            driver.back()

            # Aguarde 10 segundos antes de continuar para o próximo produto
            time.sleep(10)

        else:
            print(f"Link do produto {product_index} na página {page_number} é inválido.")
    else:
        print(f"Produto {product_index} na página {page_number} não encontrado.")

# URL da página inicial
page_number = 1
url = f'https://www.brinkemont.com.br/brinquedos/page/{page_number}/'

for page_number in range(1, 11):  # Defina o número de páginas que deseja percorrer
    # Abra a página inicial
    driver.get(url)

    # Aguarde 10 segundos para carregar a página (ajuste conforme necessário)
    time.sleep(10)

    # Loop através dos produtos na página
    for i in range(1, 51):  # Supondo que existem 100 produtos na página
        # Chame a função para coletar informações e salvar em um CSV
        collect_product_data_and_save(page_number, i)

    # Atualize a URL para a próxima página
    url = f'https://www.brinkemont.com.br/brinquedos/page/{page_number + 1}/'

# Feche o driver
driver.quit()