

with src as (

    select
        cast(id_venda      as bigint)               as id_venda,
        cast(id_produto    as int)                  as id_produto,
        cast(preco         as numeric(12,2))        as preco,
        cast(quantidade    as int)                  as quantidade,
        cast(data_venda    as date)                 as data_venda,
        cast(id_cliente    as int)                  as id_cliente,
        cast(id_loja       as int)                  as id_loja,
        cast(id_vendedor   as int)                  as id_vendedor,
        lower(trim(meio_pagamento))                 as meio_pagamento,
        cast(parcelamento  as smallint)             as parcelamento
    from "general_rtxt"."bronze"."vendas"

)

select *
from src