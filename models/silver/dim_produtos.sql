{{ config(materialized = 'table') }}

with src as (

    select
        cast(id_produto         as int)           as id_produto,
        nome_produto,
        categoria,
        cast(percentual_imposto as numeric(5,2))  as percentual_imposto
    from {{ source('bronze','produtos') }}

)

select *
from src
