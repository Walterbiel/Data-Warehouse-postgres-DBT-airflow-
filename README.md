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

## Arquitetura da Solução

- **Camada Bronze**: Recepção bruta dos dados extraídos.  
- **Camada Silver**: Dados padronizados e limpos via dbt.  
- **Camada Gold**: Modelos analíticos e tabelas agregadas.  
- **Orquestração**: Pipelines schedulados em Airflow (DAGs de ingestão, transformação e carga).  
- **Relatórios & BI**: Conectores e dashboards para Power BI (ou outra ferramenta).  
- **ML & IA**: Possibilidade de plug-and-play de modelos preditivos e alertas automatizados. :contentReference[oaicite:6]{index=6}:contentReference[oaicite:7]{index=7}

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

### 1. Pré-requisitos

- Docker & Docker Compose  
- Python 3.8+  
- PostgreSQL 13+  
- dbt Core  
- Airflow 2.x  

### 2. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/live-dw-postgres-dbt-airflow.git
cd live-dw-postgres-dbt-airflow
3. Subir os Containers
bash
Copy
Edit
docker-compose up -d
Isso iniciará:

postgres (porta 5432)

airflow webserver (porta 8080)

dbt (via CLI em um container auxiliar)

4. Configurar o dbt
No diretório dbt_project/:

Ajuste o arquivo profiles.yml com as credenciais do PostgreSQL.

Execute:

bash
Copy
Edit
dbt deps
dbt seed
dbt run
dbt test
5. Agendar DAGs no Airflow
Copie os arquivos dags/ para o volume do Airflow.

Na interface web (http://localhost:8080), habilite e dispare os DAGs de ingestão e transformação.

Uso
Ingestão & Carga: os DAGs realizam a extração do ERP e carregam os dados na camada Bronze.

Transformação: dbt executa os modelos de limpeza e padronização, populando Silver e Gold.

Relatórios: conecte-se ao schema Gold no PostgreSQL para alimentar dashboards.

Alertas: configure notificações via e-mail/Slack nos DAGs de Airflow ou no nível de BI.

Contribuição
Fork este repositório

Crie sua branch (git checkout -b feature/nova-funcionalidade)

Commit suas alterações (git commit -m 'Adiciona ...')

Push para a branch (git push origin feature/nova-funcionalidade)

Abra um Pull Request
