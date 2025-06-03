{{ config(materialized = 'table') }}

with src as (

    select
        cast(id_loja  as int)   as id_loja,
        nome_loja,
        logradouro,
        cast("numero" as int)   as numero,
        bairro,
        cidade,
        estado,
        cep
    from {{ source('bronze','lojas') }}

)

select *
from src
