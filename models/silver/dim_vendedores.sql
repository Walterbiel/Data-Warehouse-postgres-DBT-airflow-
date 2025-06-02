{{ config(materialized = 'table') }}

with src as (

    select
        cast(id                as int)   as id_vendedor,
        nome_vendedor,
        cast(data_admissao     as date)  as data_admissao,
        endereco_vendedor,
        cast(data_nascimento   as date)  as data_nascimento
    from {{ source('bronze','vendedores') }}

)

select *
from src
