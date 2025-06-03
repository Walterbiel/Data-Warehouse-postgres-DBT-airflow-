{{ config(materialized = 'view') }}

WITH base AS (
    SELECT
        DATE_TRUNC('month', data_venda)::date AS mes,
        categoria,
        SUM(receita_bruta) AS receita_mensal
    FROM {{ ref('fct_vendas') }}
    GROUP BY 1, 2
),

crescimento AS (
    SELECT
        mes,
        categoria,
        receita_mensal,
        LAG(receita_mensal) OVER (PARTITION BY categoria ORDER BY mes) AS receita_mes_anterior
    FROM base
)

SELECT
    *,
    ROUND(
        CASE
            WHEN receita_mes_anterior > 0 THEN 
                (receita_mensal - receita_mes_anterior) / receita_mes_anterior::numeric
            ELSE NULL
        END, 4
    ) AS crescimento_pct
FROM crescimento
