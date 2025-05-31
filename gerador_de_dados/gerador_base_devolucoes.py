import numpy as np
import pandas as pd

# 1) Parâmetros
TOTAL_DEVOLUCOES = 30_000
np.random.seed(42)

# 2) Seleciona aleatoriamente até 30 mil ids de venda (entre 1 e 2 milhões)
id_venda_devolvida = np.random.choice(np.arange(1, 2_000_001), size=TOTAL_DEVOLUCOES, replace=False)

# 3) Cada devolução é de 1 item aleatório daquela venda
id_produto   = np.random.randint(1, 301,   size=TOTAL_DEVOLUCOES)
id_cliente   = np.random.randint(1, 451,   size=TOTAL_DEVOLUCOES)
id_vendedor  = np.random.randint(1, 121,   size=TOTAL_DEVOLUCOES)
id_loja      = np.random.randint(1, 16,    size=TOTAL_DEVOLUCOES)

# 4) Data da devolução = data aleatória entre 1 e 30 dias após data da venda (simulada)
data_venda = pd.to_datetime(np.random.choice(
    pd.date_range(start='2018-01-01', end='2025-04-30'),



    
    size=TOTAL_DEVOLUCOES
))
dias_offset = np.random.randint(1, 31, size=TOTAL_DEVOLUCOES)
data_devolucao = data_venda + pd.to_timedelta(dias_offset, unit='D')

# 5) Preço de referência (com inflação leve desde 2018)
anos = data_venda.year
base_price = np.random.uniform(10, 780, size=TOTAL_DEVOLUCOES)
preco = np.round(base_price * (1 + 0.02 * (anos - 2018)), 2)

# 6) Quantidade devolvida (1 ou 2 itens no máximo)
quantidade = np.random.choice([1, 2], size=TOTAL_DEVOLUCOES, p=[0.8, 0.2])

# 7) Motivo da devolução
motivos = [
    "Produto danificado", "Erro no pedido", "Cliente desistiu",
    "Produto diferente do anunciado", "Outro"
]
motivo_devolucao = np.random.choice(motivos, size=TOTAL_DEVOLUCOES, p=[0.3, 0.25, 0.2, 0.15, 0.1])

# 8) DataFrame final
df_devolucao = pd.DataFrame({
    'id_venda':         id_venda_devolvida,
    'id_produto':       id_produto,
    'preco':            preco,
    'quantidade':       quantidade,
    'data_venda':       data_venda,
    'data_devolucao':   data_devolucao,
    'id_cliente':       id_cliente,
    'id_loja':          id_loja,
    'id_vendedor':      id_vendedor,
    'motivo':           motivo_devolucao
})

# 9) Salva CSV
df_devolucao.to_csv('base_devolucoes.csv', index=False)
print("✔ Arquivo 'base_devolucoes.csv' gerado com sucesso.")
