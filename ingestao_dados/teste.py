import pandas as pd
from sqlalchemy import create_engine

# Criação correta do engine com SQLAlchemy + psycopg2
engine = create_engine(
    "postgresql+psycopg2://postgresadmin:jAloy0oZD2Aks1zMjCgDDilQExPLXKCg@dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com:5432/general_rtxt"
)

# === LEITURA DOS CSVs ===
df_vendas = pd.read_csv("base_vendas_2M.csv")


df_vendas.to_sql("vendas", engine, schema="bronze", if_exists="replace", index=False)


print("✅ Todas as tabelas foram carregadas com sucesso no schema 'bronze' do PostgreSQL!")
