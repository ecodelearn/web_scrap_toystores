import os
import time
import csv
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicialize o driver do Chrome
driver = webdriver.Chrome()

# Função para coletar informações de um produto e salvar em um CSV
def collect_product_data_and_save(product_index, page):
    # Encontre todos os links de produtos
    product_links = driver.find_elements(By.XPATH, '/html/body/div[2]/div[5]/main/div/div/div[2]/div/div/div[2]/div/ul/li')

    if len(product_links) >= product_index:
        # Obtenha o link do produto com base no índice
        product_link = product_links[product_index - 1].find_element(By.XPATH, './/div/div/a[1]').get_attribute('href')

        # Verifique se o link do produto é válido
        if product_link:
            # Abra a página do produto
            driver.get(product_link)

            # Aguarde até que a página do produto seja carregada (ajuste o tempo limite conforme necessário)
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="product-name"]')))
            except TimeoutError:
                print(f"Elemento de nome do produto {product_index} não encontrado.")
                return

            # Colete os dados do produto
            try:
                product_name_element = driver.find_element(By.XPATH, '//h1[@class="product-name"]')
                product_name = product_name_element.text.strip()

                price_element = driver.find_element(By.XPATH, '//input[@id="preco_atual"]')
                price = price_element.get_attribute('value').strip()

                description_element = driver.find_element(By.XPATH, '//div[@id="descricao"]')
                description = description_element.text.strip()

                image_element = driver.find_element(By.XPATH, '/html/body/div[2]/div[7]/main/div/div/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div/img[2]')
                image_url = image_element.get_attribute('src')

                # Baixe a imagem e salve-a no diretório correspondente
                image_dir = f'pagina{page}/imagens'
                os.makedirs(image_dir, exist_ok=True)
                image_filename = f'{image_dir}/produto_{product_index}.jpg'
                with open(image_filename, 'wb') as image_file:
                    image_file.write(requests.get(image_url).content)

                # Salve os dados em um arquivo CSV com o link da imagem
                csv_filename = f'pagina{page}/produto_{product_index}.csv'
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Nome do Produto', 'Preço', 'Descrição', 'Link da Imagem']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'Nome do Produto': product_name, 'Preço': price, 'Descrição': description, 'Link da Imagem': image_filename})

            except NoSuchElementException:
                print(f"Informações do produto {product_index} não encontradas.")

            # Espere 10 segundos antes de prosseguir para o próximo nível
            time.sleep(10)

            # Volte um nível para a página da lista de produtos
            driver.back()
            time.sleep(5)

        else:
            print(f"Link do produto {product_index} é inválido.")
    else:
        print(f"Produto {product_index} não encontrado.")

# URL da página inicial
base_url = 'https://www.ninabrinquedoseducativos.com.br/loja/catalogo.php?loja=612872&categoria=12&pg='

# Loop através das páginas
for page in range(1, 13):  # Supondo que existem 12 páginas
    # Abra a página inicial
    driver.get(base_url + str(page))

    # Aguarde 10 segundos para carregar a página (ajuste conforme necessário)
    time.sleep(10)

    # Loop através dos produtos na página
    for i in range(1, 16):  # Supondo que existam 15 produtos por página
        # Chame a função para coletar informações e salvar em um CSV
        collect_product_data_and_save(i, page)

# Feche o driver
driver.quit()
