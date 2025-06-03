
  
    

  create  table "general_rtxt"."bronze_silver"."indicadores_vendas__dbt_tmp"
  
  
    as
  
  (
    

WITH base AS (
    SELECT
        data_venda,
        id_loja,
        preco,
        quantidade,
        id_venda
    FROM "general_rtxt"."bronze_gold"."fct_vendas"
)
SELECT
    data_venda,
    id_loja,
    SUM(preco * quantidade) AS receita_total,
    COUNT(DISTINCT id_venda) AS qtd_vendas
FROM base
GROUP BY data_venda, id_loja
  );
  