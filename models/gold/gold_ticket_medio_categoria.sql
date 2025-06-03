{{ config(materialized = 'view') }}

WITH base AS (
    SELECT
        DATE_TRUNC('month', data_venda)::date AS mes,
        categoria,
        SUM(receita_bruta) AS receita,
        SUM(quantidade) AS itens
    FROM {{ ref('fct_vendas') }}
    GROUP BY 1, 2
)

SELECT
    mes,
    categoria,
    receita,
    itens,
    ROUND(receita / NULLIF(itens, 0), 2) AS ticket_medio
FROM base
