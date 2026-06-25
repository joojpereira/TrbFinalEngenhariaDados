# Trabalho Final - Engenharia de Dados

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5.1-orange?logo=apachespark)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9-017CEE?logo=apacheairflow)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-3.2-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![MinIO](https://img.shields.io/badge/MinIO-S3-red)
![Superset](https://img.shields.io/badge/Apache%20Superset-Dashboard-FF6B6B)

Pipeline de dados completo com arquitetura Medalhao (Landing, Bronze, Silver, Gold) utilizando dados Northwind expandidos com Python Faker.

## Documentacao

Acesse a documentacao completa em: **https://joojpereira.github.io/TrbFinalEngenhariaDados/**

## Equipe

| Nome | GitHub |
|---|---|
| Bruno Sabino | [@SabinexX](https://github.com/SabinexX) |
| Filipe Jeremias | [@filipejeremias](https://github.com/filipejeremias) |
| Joao Vitor Pereira | [@joojpereira](https://github.com/joojpereira) |
| Nathan Frassetto | [@NathanFrassetto](https://github.com/NathanHF) |
| Rafael Pagnan | [@Ra-man](https://github.com/Ra-man) |
| Ryan Candeu | [@ryancandeu](https://github.com/ryancandeu) |

## Arquitetura do Pipeline

```text
PostgreSQL (Northwind + Faker)
            |
     Apache Airflow (Orquestracao)
            |
            v
  MinIO - landing/ (CSV)
            |
     Apache Spark
            |
            v
  MinIO - bronze/ (Delta Lake)
            |
     Apache Spark
            |
            v
  MinIO - silver/ (Delta Lake)
            |
     Apache Spark
            |
            v
  MinIO - gold/ (Delta Lake - Modelo Dimensional)
            |
            v
  Apache Superset (Dashboard)
```

## Stack Tecnologica

| Tecnologia | Versao | Finalidade |
|---|---|---|
| Python | 3.11 | Linguagem principal |
| Apache Spark (PySpark) | 3.5.1 | Transformacao dos dados |
| Apache Airflow | 2.9 | Orquestracao do pipeline |
| PostgreSQL | 15 | Banco de dados de origem |
| MinIO | latest | Object storage (Data Lake) |
| Delta Lake | 3.2 | Formato Bronze/Silver/Gold |
| Apache Superset | latest | Dashboard |
| Docker Compose | - | Containerizacao |
| MkDocs Material | - | Documentacao |

## Fonte de Dados

Schema Northwind expandido com Python Faker: 10 tabelas, 10.000+ registros por tabela, ultimos 3 anos.

Tabelas: customers, orders, order_details, products, categories, employees, suppliers, shippers, regions, territories

### Como rodar o projeto

**1. Clone o repositório:**
```bash
git clone https://github.com/joojpereira/TrbFinalEngenhariaDados.git
cd TrbFinalEngenhariaDados
```

**2. Crie o arquivo `.env` a partir do modelo:**
```bash
cp .env.example .env
```

**3. Suba o ambiente (com o Docker Desktop aberto):**
```bash
docker compose up -d
```
O Postgres cria as 10 tabelas automaticamente (via initdb) e o Airflow já cria o usuário admin no boot.

**4. Popule o Postgres com os dados de origem:**
```bash
docker run --rm --network trbfinalengenhariadados_pipeline_net \
  -v "/$(pwd)":/app -w //app python:3.11 \
  bash -c "pip install -q pandas sqlalchemy psycopg2-binary && PGHOST=postgres python sql/load_to_postgres.py"
```

**5. Crie a connection do Airflow (ingestão):**
```bash
docker exec airflow-webserver airflow connections add postgres_origem \
  --conn-uri postgresql://admin:admin123@postgres:5432/food_delivery
```

**6. Acesse as interfaces:**

As URLs e credenciais de cada serviço estão na seção [Serviços e Portas](#servicos-e-portas) abaixo.

> **Importante:** o `.env` não é versionado (contém credenciais). O passo 2 é obrigatório — sem ele, o `docker compose` não sobe.2 é obrigatório — sem ele, o `docker compose` não sobe.

## Servicos e Portas

| Servico | URL | Usuario | Senha |
|---|---|---|---|
| Airflow | http://localhost:8080 | admin | admin123 |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin123 |
| Spark Master UI | http://localhost:8081 | - | - |
| Superset | http://localhost:8088 | admin | admin123 |
| PostgreSQL | localhost:5432 | admin | admin123 |

## Estrutura do Projeto

```text
TrbFinalEngenhariaDados/
|-- Data/
|   |-- generated/          # CSVs gerados com Faker
|   +-- original/           # CSVs originais Northwind
|-- docs/                   # Documentacao MkDocs
|-- scripts/                # Scripts auxiliares
|-- sql/                    # Schema SQL
|-- src/
|   |-- ingestion/dags/     # DAGs do Airflow
|   +-- transformation/jobs/ # Jobs PySpark
|-- superset/               # Dashboard exportado
|-- docker-compose.yml
|-- .env.example
|-- mkdocs.yml
+-- README.md
```

## Camadas do Data Lake

| Camada | Formato | Descricao |
|---|---|---|
| Landing | CSV | Dados brutos do PostgreSQL |
| Bronze | Delta Lake | Dados ingeridos sem transformacao |
| Silver | Delta Lake | Dados limpos e padronizados |
| Gold | Delta Lake | Modelo dimensional para dashboard |
