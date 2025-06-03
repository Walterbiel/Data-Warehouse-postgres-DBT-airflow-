

with fct as (
    select * from "general_rtxt"."bronze_gold"."fct_vendas"
)

select
    data_venda,
    id_loja,
    nome_loja,
    sum(receita_bruta)                           as receita_diaria,
    count(distinct id_venda)                     as qtd_vendas,
    sum(quantidade)                              as itens_vendidos
from fct
group by data_venda, id_loja, nome_loja