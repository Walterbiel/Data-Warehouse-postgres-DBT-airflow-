

with fct as (
    select * from "general_rtxt"."bronze_gold"."fct_vendas"
),

base as (
    select
        date_trunc('month', data_venda)::date    as mes,
        categoria,
        sum(receita_bruta)                       as receita_mensal,
        sum(quantidade)                          as itens_vendidos
    from fct
    group by 1, 2
)

select * from base