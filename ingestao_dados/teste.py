import psycopg2
import csv

# Conexão com o PostgreSQL
conn = psycopg2.connect(
    host="dpg-d0khna8gjchc73ae1r1g-a.oregon-postgres.render.com",
    port="5432",
    database="general_rtxt",
    user="postgresadmin",
    password="jAloy0oZD2Aks1zMjCgDDilQExPLXKCg"
)
cursor = conn.cursor()

# Criação da tabela manualmente (ajuste os tipos se quiser)
cursor.execute("""
    DROP TABLE IF EXISTS bronze.vendas;
    CREATE TABLE bronze.vendas (
        id_venda INTEGER,
        id_produto INTEGER,
        preco FLOAT,
        quantidade INTEGER,
        data_venda TIMESTAMP,
        id_cliente INTEGER,
        id_loja INTEGER,
        id_vendedor INTEGER,
        meio_pagamento TEXT,
        parcelamento INTEGER
    );
""")
conn.commit()

# Copiar os dados do CSV para a tabela
with open("base_vendas_2M.csv", "r", encoding="utf-8") as f:
    next(f)  # Pular cabeçalho
    cursor.copy_expert("COPY bronze.vendas FROM STDIN WITH CSV", f)

conn.commit()
cursor.close()
conn.close()

print("✅ Dados inseridos com sucesso na tabela bronze.vendas")
