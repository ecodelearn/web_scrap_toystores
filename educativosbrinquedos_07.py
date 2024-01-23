import csv
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicialize o driver do Chrome
driver = webdriver.Chrome()

# Função para criar uma pasta com base no texto da classe "title"
def create_folder_with_title(title):
    folder_name = title.replace(' ', '_')  # Remover espaços e usar '_' no lugar
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Função para coletar informações de um produto e salvar em um arquivo CSV
def collect_product_data_and_save(product_url, product_index, page):
    try:
        # Abra a página do produto
        driver.get(product_url)
        
        product_name_element = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/h1')
        product_name = product_name_element.text.strip()

        price_element = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/strong')
        price = price_element.text.strip()

        description_element = driver.find_element(By.ID, 'descricao')
        description = description_element.text.strip()

        # Encontre a lista de elementos <li> dentro do elemento <ul> para obter as imagens
        image_elements = driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div/div/ul/li')

        # Crie uma pasta com base no texto da classe "title" e armazene as imagens lá
        folder_name = create_folder_with_title(product_name)

        image_paths = []

        # Loop para fazer o download das imagens
        for i, image_element in enumerate(image_elements, start=1):
            image_url = image_element.find_element(By.TAG_NAME, 'img').get_attribute('src')
            response = requests.get(image_url)

            if response.status_code == 200:
                image_filename = f'{folder_name}/imagem_{i}.jpg'
                with open(image_filename, 'wb') as image_file:
                    image_file.write(response.content)
                image_paths.append(image_filename)

        # Salve os dados em um arquivo CSV na pasta correspondente à página
        csv_filename = f'{folder_name}/produto_{product_index}_pagina{page}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Nome do Produto', 'Preço', 'Descrição', 'Imagens']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Nome do Produto': product_name, 'Preço': price, 'Descrição': description, 'Imagens': ', '.join(image_paths)})

    except Exception as e:
        print(f"Erro ao coletar informações do produto {product_index} na página {page}: {str(e)}")

# Função para navegar entre as páginas
def navigate_between_pages(total_pages):
    base_url = 'https://www.educativosbrinquedos.com.br/brinquedos-educativos?pagina='

    for page in range(1, total_pages + 1):
        # Abra a página inicial
        driver.get(base_url + str(page))

        # Aguarde alguns segundos para carregar a página (ajuste conforme necessário)
        time.sleep(10)

        # Encontre todos os links de produtos na página após a navegação
        product_links = driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/ul/li/div/a')

        # Crie uma lista para armazenar os links de produtos
        product_urls = [product_link.get_attribute('href') for product_link in product_links]

        # Loop através dos links de produtos
        for product_index, product_url in enumerate(product_urls, start=1):
            # Chame a função para coletar informações e salvar em um CSV
            collect_product_data_and_save(product_url, product_index, page)
            
            # Espere 10 segundos antes de voltar para a página inicial da lista de produtos
            time.sleep(10)
            driver.back()

# Chame a função para navegar entre as páginas com um total de 9 páginas
total_pages = 9
navigate_between_pages(total_pages)

# Feche o driver
driver.quit()