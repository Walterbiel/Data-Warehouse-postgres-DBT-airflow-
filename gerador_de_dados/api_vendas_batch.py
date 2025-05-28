from fastapi import FastAPI
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# ✅ Configuração da conexão PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgresadmin:jAloy0oZD2Aks1zMjCgDDilQExPLXKCg@dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com:5432/general_rtxt"
engine = create_engine(DATABASE_URL)

@app.post("/gerar_vendas")
def gerar_e_inserir_vendas():
    np.random.seed()  # dados diferentes a cada execução
    TOTAL_LINHAS = 50

    # Tamanho de vendas entre 1 e 8
    sale_sizes = np.random.randint(1, 9, size=TOTAL_LINHAS)
    sale_ids = np.arange(1, TOTAL_LINHAS + 1)

    # Colunas estáticas
    id_produto = np.random.randint(1, 301, size=TOTAL_LINHAS)
    id_cliente = np.random.randint(1, 451, size=TOTAL_LINHAS)
    id_vendedor = np.random.randint(1, 121, size=TOTAL_LINHAS)
    id_loja = np.random.randint(1, 16, size=TOTAL_LINHAS)

    # Datas de venda — últimos 30 dias
    start = pd.Timestamp.now() - pd.Timedelta(days=30)
    end = pd.Timestamp.now()
    dias = (end - start).days
    offsets = np.random.randint(0, dias + 1, size=TOTAL_LINHAS)
    data_venda = start + pd.to_timedelta(offsets, unit='D')

    anos = data_venda.year.values
    base_price = np.random.uniform(10, 780, size=TOTAL_LINHAS)
    preco = np.round(base_price * (1 + 0.02 * (anos - 2018)), 2)

    mu = 3 + 0.1 * (anos - 2018)
    q = np.random.normal(loc=mu, scale=1.5, size=TOTAL_LINHAS)
    quantidade = np.clip(np.round(q), 1, 7).astype(int)

    meios = ['dinheiro', 'cartao_debito', 'cartao_credito']
    probs = [0.5, 0.3, 0.2]
    meio_pagamento = np.random.choice(meios, size=TOTAL_LINHAS, p=probs)

    line_total = preco * quantidade
    totals_por_linha = line_total

    parcelamento = np.zeros(TOTAL_LINHAS, dtype=int)
    mask_credit = meio_pagamento == 'cartao_credito'
    parcelamento[mask_credit] = 1
    big = mask_credit & (totals_por_linha > 1000)
    parcelamento[big] = np.random.randint(1, 4, size=big.sum())

    df = pd.DataFrame({
        'idfrom fastapi import FastAPI
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# ✅ Configuração da conexão PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgresadmin:jAloy0oZD2Aks1zMjCgDDilQExPLXKCg@dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com:5432/general_rtxt"
engine = create_engine(DATABASE_URL)

@app.post("/gerar_vendas")
def gerar_e_inserir_vendas():
    np.random.seed()  # dados diferentes a cada execução
    TOTAL_LINHAS = 50

    # Tamanho de vendas entre 1 e 8
    sale_sizes = np.random.randint(1, 9, size=TOTAL_LINHAS)
    sale_ids = np.arange(1, TOTAL_LINHAS + 1)

    # Colunas estáticas
    id_produto = np.random.randint(1, 301, size=TOTAL_LINHAS)
    id_cliente = np.random.randint(1, 451, size=TOTAL_LINHAS)
    id_vendedor = np.random.randint(1, 121, size=TOTAL_LINHAS)
    id_loja = np.random.randint(1, 16, size=TOTAL_LINHAS)

    # Datas de venda — últimos 30 dias
    start = pd.Timestamp.now() - pd.Timedelta(days=30)
    end = pd.Timestamp.now()
    dias = (end - start).days
    offsets = np.random.randint(0, dias + 1, size=TOTAL_LINHAS)
    data_venda = start + pd.to_timedelta(offsets, unit='D')

    anos = data_venda.year.values
    base_price = np.random.uniform(10, 780, size=TOTAL_LINHAS)
    preco = np.round(base_price * (1 + 0.02 * (anos - 2018)), 2)

    mu = 3 + 0.1 * (anos - 2018)
    q = np.random.normal(loc=mu, scale=1.5, size=TOTAL_LINHAS)
    quantidade = np.clip(np.round(q), 1, 7).astype(int)

    meios = ['dinheiro', 'cartao_debito', 'cartao_credito']
    probs = [0.5, 0.3, 0.2]
    meio_pagamento = np.random.choice(meios, size=TOTAL_LINHAS, p=probs)

    line_total = preco * quantidade
    totals_por_linha = line_total

    parcelamento = np.zeros(TOTAL_LINHAS, dtype=int)
    mask_credit = meio_pagamento == 'cartao_credito'
    parcelamento[mask_credit] = 1
    big = mask_credit & (totals_por_linha > 1000)
    parcelamento[big] = np.random.randint(1, 4, size=big.sum())

    df = pd.DataFrame({
        'id_venda': sale_ids,
        'id_produto': id_produto,
        'preco': preco,
        'quantidade': quantidade,
        'data_venda': data_venda.dt.strftime('%Y-%m-%d'),
        'id_cliente': id_cliente,
        'id_loja': id_loja,
        'id_vendedor': id_vendedor,
        'meio_pagamento': meio_pagamento,
        'parcelamento': parcelamento
    })

    # ✅ Inserção no PostgreSQL
    try:
        df.to_sql("vendas", engine, schema="bronze", if_exists="append", index=False)
        return {"message": f"{TOTAL_LINHAS} registros inseridos com sucesso na tabela bronze.vendas."}
    except Exception as e:
        return {"error": str(e)}
eco': preco,
        'quantidade': quantidade,
        'data_venda': data_venda.dt.strftime('%Y-%m-%d'),
        'id_cliente': id_cliente,
        'id_loja': id_loja,
        'id_vendedor': id_vendedor,
        'meio_pagamento': meio_pagamento,
        'parcelamento': parcelamento
    })

    # ✅ Inserção no PostgreSQL
    try:
        df.to_sql("vendas", engine, schema="bronze", if_exists="append", index=False)
        return {"message": f"{TOTAL_LINHAS} registros inseridos com sucesso na tabela bronze.vendas."}
    except Exception as e:
        return {"error": str(e)}
