
  
    

  create  table "general_rtxt"."bronze_silver"."dim_lojas__dbt_tmp"
  
  
    as
  
  (
    

with src as (

    select
        cast(id_loja  as int)   as id_loja,
        nome_loja,
        logradouro,
        cast("número" as int)   as numero,
        bairro,
        cidade,
        estado,
        cep
    from "general_rtxt"."bronze"."lojas"

)

select *
from src
  );
  