import pandas as pd
from sqlalchemy import create_engine

# 1) Conexão SQLAlchemy 1.4.x
engine = create_engine(
    "postgresql+psycopg2://postgresadmin:jAloy0oZD2Aks1zMjCgDDilQExPLXKCg"
    "@dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com:5432/general_rtxt"
)

# 2) Arquivos de origem
excel_path = "BAses para live DW.xlsx"
csv_vendas = "base_vendas_2M.csv"
csv_devolucoes = "base_devolucoes.csv"

df_lojas      = pd.read_excel(excel_path, sheet_name="lojas")
df_produtos   = pd.read_excel(excel_path, sheet_name="produtos")
df_vendedores = pd.read_excel(excel_path, sheet_name="vendedores")
df_vendas     = pd.read_csv(csv_vendas)
df_devolucoes = pd.read_csv(csv_devolucoes)

# 3) Parâmetros comuns de carga
common = dict(
    schema="bronze",
    if_exists="append", 
    index=False,
    method="multi",
    chunksize=10_000,
)

# 4) Inserção em transação única
with engine.begin() as conn:         # abre transaction e faz commit automático
    df_lojas.to_sql("lojas", conn, **common)
    df_produtos.to_sql("produtos", conn, **common)
    df_vendedores.to_sql("vendedores", conn, **common)
    df_vendas.to_sql("vendas", conn, **common)
    df_devolucoes.to_sql("devolucoes", conn, **common)

print("✅ Carga inicial concluída — dados inseridos em bronze.* sem sobrescrever estruturas!")
