SELECT
    data_venda,
    id_loja,
    SUM(preco * quantidade) AS receita_total,
    COUNT(DISTINCT id_venda) AS qtd_vendas
FROM {{ ref('fct_vendas') }}
GROUP BY data_venda, id_loja