

with src as (

    select
        cast(id_vendedor                as int)   as id_vendedor,
        nome_vendedor,
        cast(data_admissao     as date)  as data_admissao,
        endereco_vendedor,
        cast(data_nascimento   as date)  as data_nascimento
    from "general_rtxt"."bronze"."vendedores"

)

select *
from src