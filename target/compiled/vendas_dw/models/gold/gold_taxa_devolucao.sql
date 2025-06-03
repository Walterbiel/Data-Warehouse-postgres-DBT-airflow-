

WITH vendas AS (
    SELECT id_venda, id_produto, data_venda, receita_bruta
    FROM "general_rtxt"."bronze_gold"."fct_vendas"
),
devolucoes AS (
    SELECT id_venda, data_devolucao
    FROM "general_rtxt"."bronze_gold"."fct_devolucoes"
)

SELECT
    v.data_venda,
    COUNT(DISTINCT v.id_venda) AS vendas_totais,
    COUNT(DISTINCT d.id_venda) AS vendas_devolvidas,
    ROUND(
        COUNT(DISTINCT d.id_venda)::numeric / NULLIF(COUNT(DISTINCT v.id_venda), 0),
        4
    ) AS taxa_devolucao
FROM vendas v
LEFT JOIN devolucoes d ON v.id_venda = d.id_venda
GROUP BY v.data_venda