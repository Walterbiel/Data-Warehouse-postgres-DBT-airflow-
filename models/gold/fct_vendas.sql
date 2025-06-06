{{ config(
    materialized = 'view'
) }}

WITH ventes AS (
    SELECT * FROM {{ ref('stg_vendas') }}
),

dim_produtos   AS (SELECT * FROM {{ ref('dim_produtos')   }}),
dim_lojas      AS (SELECT * FROM {{ ref('dim_lojas')      }}),
dim_vendedores AS (SELECT * FROM {{ ref('dim_vendedores') }})

SELECT
    v.id_venda,
    v.id_produto,
    v.id_loja,
    v.id_vendedor,
    v.id_cliente,
    v.data_venda,
    v.quantidade,
    v.preco,
    v.quantidade * v.preco AS receita_bruta,
    v.meio_pagamento,
    v.parcelamento,

    -- dimensões
    p.nome_produto,
    p.categoria,
    l.nome_loja,
    l.cidade,
    ve.nome_vendedor
FROM ventes v
LEFT JOIN dim_produtos   p  ON v.id_produto  = p.id_produto
LEFT JOIN dim_lojas      l  ON v.id_loja     = l.id_loja
LEFT JOIN dim_vendedores ve ON v.id_vendedor = ve.id_vendedor
