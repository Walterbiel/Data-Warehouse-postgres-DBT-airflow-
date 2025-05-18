import pandas as pd
from sqlalchemy import create_engine

# Criação correta do engine com SQLAlchemy + psycopg2
engine = create_engine(
    "postgresql+psycopg2://postgresadmin:jAloy0oZD2Aks1zMjCgDDilQExPLXKCg@dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com:5432/general_rtxt"
)

# === LEITURA DO EXCEL (várias abas) ===
excel_path = "BAses para live DW.xlsx"

df_lojas = pd.read_excel(excel_path, sheet_name="lojas")
df_produtos = pd.read_excel(excel_path, sheet_name="produtos")
df_vendedores = pd.read_excel(excel_path, sheet_name="vendedores")

# === LEITURA DOS CSVs ===
df_vendas = pd.read_csv("base_vendas_2M.csv")
df_devolucoes = pd.read_csv("base_devolucoes.csv")

# === CARGA PARA O POSTGRES - SCHEMA: bronze ===
df_lojas.to_sql("lojas", engine, schema="bronze", if_exists="replace", index=False)
df_produtos.to_sql("produtos", engine, schema="bronze", if_exists="replace", index=False)
df_vendedores.to_sql("vendedores", engine, schema="bronze", if_exists="replace", index=False)
df_vendas.to_sql("vendas", engine, schema="bronze", if_exists="replace", index=False)
df_devolucoes.to_sql("devolucoes", engine, schema="bronze", if_exists="replace", index=False)

print("✅ Todas as tabelas foram carregadas com sucesso no schema 'bronze' do PostgreSQL!")
