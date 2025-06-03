{{ config(materialized = 'view') }}

with devol as (
    select * from {{ ref('stg_devolucoes') }}
)

select
    id_venda,
    id_produto,
    id_loja,
    id_vendedor,
    id_cliente,
    data_venda,
    data_devolucao,
    quantidade,
    preco,
    quantidade * preco                             as valor_devolvido,
    motivo
from devol
