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
   - Armazenamento em estrutura analítica (Data Warehouse ou Lakehouse). :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

2. **Análises Essenciais**  
   - Resumo diário de vendas (quantidade, faturamento, ticket médio por loja, canal e produto).  
   - Ruptura e giro de estoque (estoque zerado, tempo médio de reposição, giro por categoria).  
   - Status da produção (ordens em aberto, em atraso, produção por linha/fábrica).  
   - Comparativo Real × Meta (metas comerciais por equipe, linha de produto e período).  
   - Alertas operacionais para desvios em vendas, estoque ou produção. :contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}

3. **Visualização e Ações**  
   - Dashboard unificado com painéis interativos para vendas, estoque e produção, acessível em desktop e mobile.  
   - Filtros dinâmicos por período, filial, produto, categoria e canal.  
   - Alertas automatizados (e-mail/WhatsApp) para eventos críticos.  
   - Exportação de relatórios (Excel/PDF) para reuniões estratégicas. :contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}

---

## Tecnologias

- **Banco de Dados**  
  - PostgreSQL (DW)  
- **Transformação de Dados**  
  - [dbt](https://www.getdbt.com/)  
- **Orquestração**  
  - [Apache Airflow](https://airflow.apache.org/)  
- **Visualização**  
  - Power BI / ferramentas compatíveis  
- **Complementares**  
  - Python (scripts de ingestão, testes e helpers)  
  - Docker (ambientes isolados)  

---

## Como Começar
1.Importe os dados disponibilizados para a pasta principal do projeto.

2. Crie um ambiente virtual com o comando:
python -m venv .venv

Ative o ambiente: source .venv/bin/activate

3. Instale as dependências necessarias para o projeto:
pip install -r requirements.txt

4.Subir container docker para airflow e dbt
docker compose --env-file .env up

