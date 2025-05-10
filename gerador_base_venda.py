import numpy as np
import pandas as pd

# 1) Parâmetros gerais
TOTAL_LINHAS = 2_000_000
np.random.seed(42)

# 2) Geração dos tamanhos de venda (1–8 itens) até somar ~2M
sale_sizes = []
total = 0
while total < TOTAL_LINHAS:
    s = np.random.randint(1, 9)
    sale_sizes.append(s)
    total += s

# Ajusta para exatamente TOTAL_LINHAS e conta quantas vendas virão
sale_ids = np.repeat(np.arange(1, len(sale_sizes)+1), sale_sizes)[:TOTAL_LINHAS]
sale_sizes = sale_sizes[:len(np.unique(sale_ids))]
n = sale_ids.size

# 3) Preenche colunas estáticas
id_produto   = np.random.randint(1, 301,   size=n)
id_cliente   = np.random.randint(1, 451,   size=n)
id_vendedor  = np.random.randint(1, 121,   size=n)
id_loja      = np.random.randint(1, 16,    size=n)

# 4) Datas de venda uniformes entre 2018-01-01 e 2025-04-30
start = np.datetime64('2018-01-01')
end   = np.datetime64('2025-04-30')
dias  = (end - start).astype(int)
offsets = np.random.randint(0, dias+1, size=n)
data_venda = start + offsets.astype('timedelta64[D]')

# 5) Extrai o ano para simular tendência de crescimento
anos = pd.to_datetime(data_venda).year.values

# 6) Preço: uniform(10,780) com +2% a mais a cada ano desde 2018
base_price = np.random.uniform(10, 780, size=n)
preco = np.round(base_price * (1 + 0.02 * (anos - 2018)), 2)

# 7) Quantidade: normal(μ=3 + 0.1*(ano-2018), σ=1.5), truncada em 1–7
mu = 3 + 0.1 * (anos - 2018)
q = np.random.normal(loc=mu, scale=1.5, size=n)
quantidade = np.clip(np.round(q), 1, 7).astype(int)

# 8) Meio de pagamento
meios = ['dinheiro', 'cartao_debito', 'cartao_credito']
probs = [0.5, 0.3, 0.2]
meio_pagamento = np.random.choice(meios, size=n, p=probs)

# 9) Cálculo de total por item e parcelamento
line_total = preco * quantidade

# 9a) soma total por venda (id_venda está ordenado, grupos contíguos)
boundaries     = np.concatenate(([0], np.cumsum(sale_sizes)[:-1]))
sale_totals    = np.add.reduceat(line_total, boundaries)
totals_por_linha = np.repeat(sale_totals, sale_sizes)[:n]

# 9b) parcelamento: 0 por padrão, 1 se cartao_credito, e 1–3 se >1000
parcelamento = np.zeros(n, dtype=int)
mask_credit  = meio_pagamento == 'cartao_credito'
parcelamento[mask_credit] = 1
big = mask_credit & (totals_por_linha > 1000)
parcelamento[big] = np.random.randint(1, 4, size=big.sum())

# 10) Monta DataFrame e salva CSV
df = pd.DataFrame({
    'id_venda':         sale_ids,
    'id_produto':       id_produto,
    'preco':            preco,
    'quantidade':       quantidade,
    'data_venda':       pd.to_datetime(data_venda),
    'id_cliente':       id_cliente,
    'id_loja':          id_loja,
    'id_vendedor':      id_vendedor,
    'meio_pagamento':   meio_pagamento,
    'parcelamento':     parcelamento
})

df.to_csv('/mnt/data/base_vendas_2M.csv', index=False)
print("CSV gerado em /mnt/data/base_vendas_2M.csv")```

**O que o script faz**  
- Cria vendas com de 1 a 8 itens cada (totalizando ~2 000 000 linhas).  
- A coluna `preco` cresce 2% ao ano em média (simulando inflação).  
- A `quantidade` média sobe 0.1 item por ano (distribuição normal).  
- Define `meio_pagamento` com as três categorias e calcula `parcelamento` de acordo com o total da venda.  
- Usa nomes snake_case e datas entre 01/01/2018 e 30/04/2025.

Basta rodar esse script no seu Python local ou no notebook, e ele já vai gerar a base para você carregar no seu ETL/Data Warehouse.
