import requests

# Lista de URLs para raspar
urls = [
    "https://www.rihappy.com.br/",
    "https://www.ideiariabrinquedos.com.br",
    "https://www.ioiodepano.com.br",
    "https://www.ninabrinquedoseducativos.com.br",
    "https://www.amorludico.com.br",
    "https://www.balloonbrinquedos.com.br",
    "https://www.bambinno.com.br",
    "https://www.brinkemont.com.br",
    "https://www.cabanadodesenvolvimento.com.br",
    "https://www.casadobrinquedo.com.br",
    "https://www.catataubrinquedos.com.br",
    "https://www.costurandobrincadeiras.com.br",
    "https://www.dinobailarino.com.br",
    "https://www.fabricadecasinha.com.br",
    "https://www.fabricaideiasparacriancas.com.br",
    "https://www.lalukabrinquedos.com.br",
    "https://www.lojakurumim.com.br",
    "https://www.ludiquedesign.com.br",
    "https://www.ludolica.com.br",
    "https://www.majocacolore.com.br",
    "https://www.minicientista.com.br",
    "https://www.mundoekko.com.br",
    "https://www.peggui.com.br",
    "https://www.pikoli.com.br",
    "https://www.pingubrinquedos.com.br",
    "https://www.plantandoebrincando.com.br",
    "https://www.primaveracriativa.com.br",
    "https://www.totem1244.rihappy.com.br",
    "https://www.wolfpetit.com.br",
    "https://www.educativosbrinquedos.com.br"
]

def check_robots_txt(url):
    try:
        # Concatena '/robots.txt' ao URL base
        robots_url = url.rstrip('/') + '/robots.txt'
        
        # Faz a requisição ao arquivo robots.txt
        response = requests.get(robots_url)

        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            print(f"Robots.txt de {url}:")
            print(response.text)
            print("-----")
        else:
            print(f"Robots.txt não encontrado ou acesso negado em {url}")

    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")

# Verifica o robots.txt de cada URL
for url in urls:
    check_robots_txt(url)
