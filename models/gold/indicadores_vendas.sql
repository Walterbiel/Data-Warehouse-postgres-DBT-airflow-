{{ 
  config(
    materialized = 'table',
    schema       = 'silver'
  ) 
}}

WITH base AS (
    SELECT
        data_venda,
        id_loja,
        preco,
        quantidade,
        id_venda
    FROM {{ ref('fct_vendas') }}
)
SELECT
    data_venda,
    id_loja,
    SUM(preco * quantidade) AS receita_total,
    COUNT(DISTINCT id_venda) AS qtd_vendas
FROM base
GROUP BY data_venda, id_loja
