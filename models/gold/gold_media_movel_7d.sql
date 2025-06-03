{{ config(materialized = 'view') }}

WITH receita_diaria AS (
    SELECT
        data_venda,
        id_loja,
        nome_loja,
        SUM(receita_bruta) AS receita_diaria
    FROM {{ ref('fct_vendas') }}
    GROUP BY data_venda, id_loja, nome_loja
)

SELECT
    *,
    AVG(receita_diaria) OVER (
        PARTITION BY id_loja
        ORDER BY data_venda
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS media_movel_7d
FROM receita_diaria
