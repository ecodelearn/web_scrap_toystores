import os
import pandas as pd

# Diretório onde os arquivos CSV estão localizados
diretorio = "./seu_diretorio/"

# Lista todos os arquivos no diretório
arquivos_csv = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(".csv")]

# Crie um DataFrame vazio para armazenar os dados combinados
dados_combinados = pd.DataFrame()

# Loop para ler e juntar todos os arquivos CSV no diretório
for arquivo in arquivos_csv:
    caminho_arquivo = os.path.join(diretorio, arquivo)
    df = pd.read_csv(caminho_arquivo)
    dados_combinados = dados_combinados.append(df, ignore_index=True)

# Salvar os dados combinados em um único arquivo CSV
dados_combinados.to_csv("arquivo_combinado.csv", index=False)