import pandas as pd
import random

# Caminho para o arquivo CSV exportado do Google Forms ou similar
caminho_arquivo = 'respostas.csv'

# Leitura da planilha
df = pd.read_csv(caminho_arquivo)

# Remover nomes nulos e duplicados
nomes = df['Seu nome completo:'].dropna().drop_duplicates().tolist()

# Verifica se há pelo menos 3 nomes para sortear
if len(nomes) < 3:
    print(f"Apenas {len(nomes)} nome(s) disponível(is) para sorteio: {nomes}")
else:
    sorteados = random.sample(nomes, 3)
    print("🎉 Nomes sorteados:")
    for nome in sorteados:
        print("-", nome)
