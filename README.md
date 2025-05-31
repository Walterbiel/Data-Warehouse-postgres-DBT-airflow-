
# Live Data Warehouse (PostgreSQL, dbt & Airflow)

Em parceria com a **3D Universe Creators** — sorteio de logos em impressão 3D de Power BI e Python

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
# Clone o projeto e entre no diretório
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. Gerar uma chave para criptografia (opcional para dbt)

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Crie as pastas necessárias

```bash
mkdir -p dags logs plugins dbt
```

---

## Orquestração com Apache Airflow (sem Docker)

### 1. Defina as variáveis de ambiente

```bash
export AIRFLOW_HOME=$(pwd)/airflow
AIRFLOW_VERSION=2.8.1
PYTHON_VERSION=$(python --version | cut -d " " -f2 | cut -d "." -f1,2)
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

### 2. Instale o Airflow

```bash
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### 3. Inicialize o Airflow e crie o usuário

```bash
airflow db init

airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### 4. Inicie o Airflow

Em dois terminais diferentes:

**Terminal 1 – Scheduler**
```bash
source .venv/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow
airflow scheduler
```

**Terminal 2 – Webserver**
```bash
source .venv/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow
airflow webserver --port 8080
```

Acesse no navegador: [http://localhost:8080](http://localhost:8080)

---

## Execução Local de Geração de Dados (FastAPI)

### 1. Execute o gerador de dados com Uvicorn

```bash
uvicorn gerador_de_dados.api_vendas_batch:app --reload --port 8002
```

---

## Execução com Docker (opcional)

### 1. Login no GitHub Container Registry (GHCR)

```bash
echo <SEU_GITHUB_TOKEN> | docker login ghcr.io -u <SEU_USUARIO_GITHUB> --password-stdin
```

> Geração do token: GitHub > Settings > Developer Settings > Personal Access Tokens  
> Permissões necessárias: ✅ `read:packages`

### 2. Subir os containers (Airflow + dbt)

```bash
docker compose --env-file .env up
```

---

## Observações

- O projeto está pronto para rodar **Airflow localmente ou via Docker**.
- Recomendado: PostgreSQL como banco de metadados do Airflow em produção.
- O SQLite é usado aqui apenas para fins educacionais.

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

---

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

### 5. Exemplo de Modelo Bronze

`models/bronze/vendas.sql`:

```sql
SELECT * FROM {{ source('bronze', 'vendas') }}
```

---

### 6. Exemplo de Modelo Silver

`models/silver/fct_vendas.sql`:

```sql
WITH vendas_clean AS (
    SELECT
        id_venda,
        id_produto,
        preco,
        quantidade,
        data_venda::date AS data_venda,
        id_cliente,
        id_loja,
        id_vendedor,
        meio_pagamento,
        parcelamento
    FROM {{ ref('vendas') }}
)
SELECT * FROM vendas_clean
```

---

### 7. Exemplo de Modelo Gold

`models/gold/indicadores_vendas.sql`:

```sql
SELECT
    data_venda,
    id_loja,
    SUM(preco * quantidade) AS receita_total,
    COUNT(DISTINCT id_venda) AS qtd_vendas
FROM {{ ref('fct_vendas') }}
GROUP BY data_venda, id_loja
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

## 🎯 Objetivos da Live

- Demonstrar como estruturar um DW do zero com dados transacionais.
- Aplicar boas práticas de modelagem dimensional.
- Apresentar o fluxo de camadas (bronze → silver → gold) com dbt.
- Mostrar indicadores de negócio em SQL a partir da camada gold.

---

## 🧠 Autor

**Walter Gonzaga**  
Data Architect | Engenheiro de Dados | Mentor  
[LinkedIn](https://www.linkedin.com/in/waltergonzaga)

---