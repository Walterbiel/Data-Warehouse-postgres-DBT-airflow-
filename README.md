
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