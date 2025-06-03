

WITH src AS (

    SELECT
        CAST(id_venda       AS BIGINT)        AS id_venda,
        CAST(id_produto     AS INTEGER)       AS id_produto,
        CAST(preco          AS NUMERIC(12,2)) AS preco,
        CAST(quantidade     AS INTEGER)       AS quantidade,
        CAST(data_venda     AS DATE)          AS data_venda,
        CAST(id_cliente     AS INTEGER)       AS id_cliente,
        CAST(id_loja        AS INTEGER)       AS id_loja,
        CAST(id_vendedor    AS INTEGER)       AS id_vendedor,
        LOWER(TRIM(meio_pagamento))           AS meio_pagamento,
        CAST(parcelamento   AS SMALLINT)      AS parcelamento
    FROM "general_rtxt"."bronze"."vendas"

    
      WHERE id_venda NOT IN (
        SELECT id_venda FROM "general_rtxt"."bronze_silver"."stg_vendas"
      )
    

)

SELECT *
FROM src