{{ config(materialized = 'table') }}

with ventes as (
    select * from {{ ref('stg_vendas') }}
),

dim_produtos   as (select * from {{ ref('dim_produtos')   }} ),
dim_lojas      as (select * from {{ ref('dim_lojas')      }} ),
dim_vendedores as (select * from {{ ref('dim_vendedores') }} )

select
    v.id_venda,
    v.id_produto,
    v.id_loja,
    v.id_vendedor,
    v.id_cliente,
    v.data_venda,
    v.quantidade,
    v.preco,
    v.quantidade * v.preco                                   as receita_bruta,
    v.meio_pagamento,
    v.parcelamento,

    -- dimensões
    p.nome_produto,
    p.categoria,
    l.nome_loja,
    l.cidade,
    ve.nome_vendedor
from ventes v
left join dim_produtos   p  on v.id_produto  = p.id_produto
left join dim_lojas      l  on v.id_loja     = l.id_loja
left join dim_vendedores ve on v.id_vendedor = ve.id_vendedor
