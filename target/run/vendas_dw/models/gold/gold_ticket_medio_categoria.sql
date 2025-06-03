
  create view "general_rtxt"."bronze_gold"."gold_ticket_medio_categoria__dbt_tmp"
    
    
  as (
    

WITH base AS (
    SELECT
        DATE_TRUNC('month', data_venda)::date AS mes,
        categoria,
        SUM(receita_bruta) AS receita,
        SUM(quantidade) AS itens
    FROM "general_rtxt"."bronze_gold"."fct_vendas"
    GROUP BY 1, 2
)

SELECT
    mes,
    categoria,
    receita,
    itens,
    ROUND(receita / NULLIF(itens, 0), 2) AS ticket_medio
FROM base
  );