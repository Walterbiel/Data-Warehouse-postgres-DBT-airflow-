
  
    

  create  table "general_rtxt"."bronze_gold"."fct_vendas__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    id_venda,
    id_produto,
    preco,
    quantidade,
    CAST(data_venda AS date) AS data_venda,
    id_cliente,
    id_loja,
    id_vendedor,
    meio_pagamento,
    parcelamento
FROM "general_rtxt"."bronze"."vendas"
  );
  