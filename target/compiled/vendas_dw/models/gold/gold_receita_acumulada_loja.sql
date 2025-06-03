

WITH base AS (
    SELECT
        data_venda,
        id_loja,
        nome_loja,
        EXTRACT(YEAR FROM data_venda) AS ano,
        receita_bruta
    FROM "general_rtxt"."bronze_gold"."fct_vendas"
),

acumulado AS (
    SELECT
        data_venda,
        id_loja,
        nome_loja,
        ano,
        SUM(receita_bruta) OVER (
            PARTITION BY id_loja, ano ORDER BY data_venda
        ) AS receita_acumulada
    FROM base
)

SELECT * FROM acumulado