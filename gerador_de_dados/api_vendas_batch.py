from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

app = FastAPI()

# Função auxiliar para gerar e inserir vendas
def gerar_e_inserir_vendas():
    N_LINHAS = 500
    np.random.seed(datetime.now().microsecond)

    # 1) Geração de venda simulada
    sale_sizes = []
    total = 0
    while total < N_LINHAS:
        s = np.random.randint(1, 9)
        sale_sizes.append(s)
        total += s

    sale_ids = np.repeat(np.arange(1, len(sale_sizes)+1), sale_sizes)[:N_LINHAS]
    sale_sizes = sale_sizes[:len(np.unique(sale_ids))]
    n = sale_ids.size

    id_produto   = np.random.randint(1, 301, size=n)
    id_cliente   = np.random.randint(1, 451, size=n)
    id_vendedor  = np.random.randint(1, 121, size=n)
    id_loja      = np.random.randint(1, 16, size=n)
    data_venda   = np.full(n, datetime.today().date(), dtype='datetime64[D]')
    anos         = pd.to_datetime(data_venda).year.values
    base_price   = np.random.uniform(10, 780, size=n)
    preco        = np.round(base_price * (1 + 0.02 * (anos - 2018)), 2)
    mu           = 3 + 0.1 * (anos - 2018)
    q            = np.random.normal(loc=mu, scale=1.5, size=n)
    quantidade   = np.clip(np.round(q), 1, 7).astype(int)
    meios        = ['dinheiro', 'cartao_debito', 'cartao_credito']
    probs        = [0.5, 0.3, 0.2]
    meio_pagamento = np.random.choice(meios, size=n, p=probs)

    line_total = preco * quantidade
    boundaries = np.concatenate(([0], np.cumsum(sale_sizes)[:-1]))
    sale_totals = np.add.reduceat(line_total, boundaries)
    totals_por_linha = np.repeat(sale_totals, sale_sizes)[:n]

    parcelamento = np.zeros(n, dtype=int)
    mask_credit = meio_pagamento == 'cartao_credito'
    parcelamento[mask_credit] = 1
    big = mask_credit & (totals_por_linha > 1000)
    parcelamento[big] = np.random.randint(1, 4, size=big.sum())

    dados = list(zip(
        id_produto.astype(int).tolist(),
        preco.astype(float).tolist(),
        quantidade.astype(int).tolist(),
        [d.item().strftime("%Y-%m-%d") for d in data_venda],
        id_cliente.astype(int).tolist(),
        id_loja.astype(int).tolist(),
        id_vendedor.astype(int).tolist(),
        meio_pagamento.tolist(),
        parcelamento.astype(int).tolist()
    ))

    # 2) Conecta e insere no PostgreSQL
    conn = psycopg2.connect(
        dbname="general_rtxt",
        user="postgresadmin",
        password="jAloy0oZD2Aks1zMjCgDDilQExPLXKCg",
        host="dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com",
        port="5432"
    )
    cur = conn.cursor()

    sql = """
        INSERT INTO bronze.vendas (
            id_produto, preco, quantidade, data_venda,
            id_cliente, id_loja, id_vendedor,
            meio_pagamento, parcelamento
        )
        VALUES %s
    """

    execute_values(cur, sql, dados)
    conn.commit()
    cur.close()
    conn.close()

    return {"status": "sucesso", "registros_inseridos": n}

# Endpoint POST para gerar dados
@app.post("/gerar-vendas")
def gerar_vendas_endpoint():
    resultado = gerar_e_inserir_vendas()
    return resultado
