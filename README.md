
# Live Data Warehouse (PostgreSQL, dbt & Airflow)

Em parceria com a **3D Universe Creators** — sorteio de logos em impressão 3D de Power BI e Python

## 💡 Recomendado para Windows
Se estiver usando Windows, o melhor cenário é:

Usar o WSL2 (Subsistema Linux do Windows) com uma distro como Ubuntu.

Você roda tudo como se estivesse em um Linux real, incluindo Docker, dbt, Airflow, PostgreSQL e VS Code com integração total.

---

## Visão Geral

Este projeto demonstra a construção de um **Data Warehouse** completo utilizando **PostgreSQL** como banco relacional, **dbt** para transformação de dados e **Apache Airflow** para orquestração de pipelines. O objetivo é atender às necessidades de integração, tratamento, análise e visualização de dados para áreas de vendas, estoque e produção.

---

## Requisitos de Negócio

1. **Coleta e Integração de Dados**  
   - Integração automática com sistemas ERP para capturar tabelas de vendas, estoque e ordens de produção, com atualização diária ou em tempo real.  
   - Tratamento e padronização (nomes de produtos, datas, filiais, centros de custo).  
   - Armazenamento em estrutura analítica (Data Warehouse ou Lakehouse).

2. **Análises Essenciais**  
   - Resumo diário de vendas (quantidade, faturamento, ticket médio por loja, canal e produto).  
   - Ruptura e giro de estoque (estoque zerado, tempo médio de reposição, giro por categoria).  
   - Status da produção (ordens em aberto, em atraso, produção por linha/fábrica).  
   - Comparativo Real × Meta (metas comerciais por equipe, linha de produto e período).  
   - Alertas operacionais para desvios em vendas, estoque ou produção.

3. **Visualização e Ações**  
   - Dashboard unificado com painéis interativos para vendas, estoque e produção, acessível em desktop e mobile.  
   - Filtros dinâmicos por período, filial, produto, categoria e canal.  
   - Alertas automatizados (e-mail/WhatsApp) para eventos críticos.  
   - Exportação de relatórios (Excel/PDF) para reuniões estratégicas.

---

## Como Começar

### 1. Preparação do Projeto

```bash

# Crie um ambiente virtual
python3.11 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

```

### 2. Gerar uma chave para criptografia (opcional para dbt)

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Crie as pastas necessárias

```bash
mkdir -p  logs plugins dbt
```
#### 4. Gerar dados fake e subir dados para o postgres

# Scripts DDL – Camada **bronze**

> **Execute** estes comandos no PostgreSQL antes da ingestão.  
> Cada tabela recebe uma chave primária surrogate (`BIGSERIAL`) iniciando em 1.

---

## 1. Criar schema

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
```

---

## 2. Tabela `bronze.vendas`

```sql
CREATE TABLE IF NOT EXISTS bronze.vendas (
    pk_vendas       BIGSERIAL PRIMARY KEY,
    id_venda        BIGINT        NOT NULL,
    id_produto      INTEGER       NOT NULL,
    preco           NUMERIC(12,2) NOT NULL,
    quantidade      INTEGER       NOT NULL,
    data_venda      DATE          NOT NULL,
    id_cliente      INTEGER,
    id_loja         INTEGER,
    id_vendedor     INTEGER,
    meio_pagamento  TEXT,
    parcelamento    SMALLINT
);

CREATE INDEX IF NOT EXISTS idx_vendas_id_venda ON bronze.vendas (id_venda);
CREATE INDEX IF NOT EXISTS idx_vendas_data     ON bronze.vendas (data_venda);
CREATE INDEX IF NOT EXISTS idx_vendas_produto  ON bronze.vendas (id_produto);
```

---

## 3. Tabela `bronze.devolucoes`

```sql
CREATE TABLE IF NOT EXISTS bronze.devolucoes (
    pk_devolucao    BIGSERIAL PRIMARY KEY,
    id_venda        BIGINT    NOT NULL,
    id_produto      INTEGER   NOT NULL,
    preco           NUMERIC(12,2) NOT NULL,
    quantidade      INTEGER   NOT NULL,
    data_venda      DATE      NOT NULL,
    data_devolucao  DATE      NOT NULL,
    id_cliente      INTEGER,
    id_loja         INTEGER,
    id_vendedor     INTEGER,
    motivo          TEXT,
    UNIQUE (id_venda, id_produto)
);

CREATE INDEX IF NOT EXISTS idx_dev_data_devolucao
    ON bronze.devolucoes (data_devolucao);
```

---

## 4. Tabela `bronze.produtos`

```sql
CREATE TABLE IF NOT EXISTS bronze.produtos (
    pk_produto          BIGSERIAL PRIMARY KEY,
    id_produto          INTEGER UNIQUE NOT NULL,
    nome_produto        TEXT    NOT NULL,
    categoria           TEXT,
    percentual_imposto  NUMERIC(5,2)
);
```

---

## 5. Tabela `bronze.lojas`

```sql
CREATE TABLE IF NOT EXISTS bronze.lojas (
    pk_loja     BIGSERIAL PRIMARY KEY,
    id_loja     INTEGER UNIQUE NOT NULL,
    nome_loja   TEXT    NOT NULL,
    logradouro  TEXT,
    numero      INTEGER,
    bairro      TEXT,
    cidade      TEXT,
    estado      CHAR(2),
    cep         VARCHAR(10)
);
```

---

## 6. Tabela `bronze.vendedores`

```sql
CREATE TABLE IF NOT EXISTS bronze.vendedores (
    pk_vendedor     BIGSERIAL PRIMARY KEY,
    id_vendedor     INTEGER UNIQUE NOT NULL,
    nome_vendedor   TEXT    NOT NULL,
    data_admissao   DATE,
    endereco_vendedor TEXT,
    data_nascimento DATE
);
```
---

# 📁 Estrutura das Tabelas na Camada Bronze

As seguintes tabelas estão disponíveis no banco PostgreSQL, no schema `bronze`:

- `vendas`: informações de vendas realizadas.
- `devolucoes`: registros de devoluções de vendas.
- `produtos`: catálogo de produtos com categoria e impostos.
- `lojas`: dados cadastrais das lojas.
- `vendedores`: cadastro de vendedores e datas importantes.

---

## 🔧 Configuração do dbt (Data Build Tool)

Este projeto utiliza o **dbt** para organizar e transformar os dados da camada bronze até a gold. Abaixo estão os passos completos para configuração e execução:

### 1. Inicialização do Projeto

```bash
dbt init vendas_dw
```

Siga os prompts e selecione o adaptador `Postgres`.

---

### 2. Estrutura Esperada do Projeto

```text
vendas_dw/
├── dbt_project.yml
├── models/
│   ├── bronze/
│   │   ├── vendas.sql
│   │   ├── devolucoes.sql
│   │   ├── produtos.sql
│   │   ├── lojas.sql
│   │   └── vendedores.sql
│   ├── silver/
│   │   ├── fct_vendas.sql
│   │   ├── fct_devolucoes.sql
│   │   └── dim_lojas.sql
│   ├── gold/
│   │   ├── indicadores_vendas.sql
│   │   └── produtos_mais_devolvidos.sql
│   └── _sources.yml
```

---

### 3. Configuração do Profile

Crie ou edite o arquivo `~/.dbt/profiles.yml`:

```yaml
vendas_dw:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: seu_usuario
      password: sua_senha
      port: 5432
      dbname: seu_banco
      schema: bronze
      threads: 4
```
bash (mover profile.yml)
```
mkdir -p ~/.dbt
code ~/.dbt/profiles.yml
```

---

### testar a conexão:
```
dbt debug --project-dir vendas_dw
```

### 4. Registro de Tabelas de Origem

`models/_sources.yml`:

```yaml
version: 2

sources:
  - name: bronze
    database: seu_banco
    schema: bronze
    tables:
      - name: vendas
      - name: devolucoes
      - name: produtos
      - name: lojas
      - name: vendedores
```

---

### 8. Executando o Projeto

Para compilar e rodar os modelos:

```bash
dbt run
```

Para validar a conexão e estrutura:

```bash
dbt debug
```

---

---

## 🗂️ Estrutura de diretórios

```
models/
├─ sources.yml               # definição das fontes bronze
├─ silver/
│  ├─ stg_vendas.sql
│  ├─ stg_devolucoes.sql
│  ├─ dim_produtos.sql
│  ├─ dim_lojas.sql
│  └─ dim_vendedores.sql
└─ gold/
   ├─ fct_vendas.sql
   ├─ fct_devolucoes.sql
   ├─ mart_receita_diaria_loja.sql
   └─ mart_receita_mensal_categoria.sql
```

> **Materialização**  
> - Todos os modelos usam `{{ config(materialized='table') }}`.  
> - Os *schemas* (**bronze**, **silver**, **gold**) são definidos no `project.yaml`.

---

## 4  🚀 Execução sugerida para a aula

```bash
# 1) Materializar staging
dbt run --select silver

# 2) Materializar fatos e marts
dbt run --select gold

# 3) Explorar lineage
dbt docs generate
dbt docs serve
```

------------------------------------------------------------------------------------------

### Rodar no postgres:

## ⚙️ Execução
Execute os comandos abaixo em sua instância PostgreSQL, ajustando os nomes dos schemas e tabelas conforme necessário.

---
## 🔹 Queries por Categoria

### 📂 Transformações de Dimensões

#### 🧾 dim_lojas.sql

```sql
-- {{ config(materialized = 'table') -- }}

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
    from -- {{ source('bronze','lojas') -- }}

)

select *
from src
```

#### 🧾 dim_produtos.sql

```sql
-- {{ config(materialized = 'table') -- }}

with src as (

    select
        cast(id_produto         as int)           as id_produto,
        nome_produto,
        categoria,
        cast(percentual_imposto as numeric(5,2))  as percentual_imposto
    from -- {{ source('bronze','produtos') -- }}

)

select *
from src
```

#### 🧾 dim_vendedores.sql

```sql
-- {{ config(materialized = 'table') -- }}

with src as (

    select
        cast(id_vendedor                as int)   as id_vendedor,
        nome_vendedor,
        cast(data_admissao     as date)  as data_admissao,
        endereco_vendedor,
        cast(data_nascimento   as date)  as data_nascimento
    from -- {{ source('bronze','vendedores') -- }}

)

select *
from src
```

### 📂 Preparação### 3.1  `fct_vendas.sql` — fluxo simplificado
```mermaid
graph TD
    subgraph Silver
        A(stg_vendas) -->|FK| B(dim_produtos)
        A -->|FK| C(dim_lojas)
        A -->|FK| D(dim_vendedores)
    end
    A -->|JOIN| E(fct_vendas - Gold)
```

### 3.2  `mart_receita_diaria_loja.sql`
```sql
select
    data_venda,
    id_loja,
    nome_loja,
    sum(receita_bruta) as receita_diaria,
    count(distinct id_venda) as qtd_vendas,
    sum(quantidade) as itens_vendidos
from {{ ref('fct_vendas') }}
group by data_venda, id_loja, nome_loja;
```
> **Uso**: Painéis operacionais (metas diárias, comparativo de lojas).
 e Limpeza da Staging

#### 🧾 stg_vendas.sql

```sql
-- {{ config(
    materialized = 'incremental',
    unique_key = 'id_venda'
) -- }}

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
        CAST(parc### 3.1  `fct_vendas.sql` — fluxo simplificado
```mermaid
graph TD
    subgraph Silver
        A(stg_vendas) -->|FK| B(dim_produtos)
        A -->|FK| C(dim_lojas)
        A -->|FK| D(dim_vendedores)
    end
    A -->|JOIN| E(fct_vendas - Gold)
```

### 3.2  `mart_receita_diaria_loja.sql`
```sql
select
    data_venda,
    id_loja,
    nome_loja,
    sum(receita_bruta) as receita_diaria,
    count(distinct id_venda) as qtd_vendas,
    sum(quantidade) as itens_vendidos
from {{ ref('fct_vendas') }}
group by data_venda, id_loja, nome_loja;
```
> **Uso**: Painéis operacionais (metas diárias, comparativo de lojas).
elamento   AS SMALLINT)      AS parcelamento
    FROM -- {{ source('bronze', 'vendas') -- }}
