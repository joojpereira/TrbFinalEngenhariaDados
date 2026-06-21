# Trabalho Final - Engenharia de Dados

Pipeline de dados completo com arquitetura medalhao (Landing, Bronze, Silver, Gold), utilizando dados de Food Delivery.

## Equipe

- Bruno Sabino
- Filipe Jeremias
- João Vitor Pereira
- Nathan Frassetto
- Rafael Pagnan
- Ryan Candeu

## Arquitetura
PostgreSQL (origem)
|
Airflow (orquestracao)
|
MinIO - landing/(dados brutos: CSV
Apache Spar
|
MinIO - bronze/(Delta Lake - dados brutos)
|
Apache Spark
|
MinIO - silver/(Delta Lake - dados limpos)
|
Apache Spark
|
MinIO - gold/(Delta Lake - modelo dimensional)
|
Apache Superset (dashboard)
## Stack Tecnologica

| Camada | Ferramenta |
|---|---|
| Banco de origem | PostgreSQL 15 |
| Orquestracao | Apache Airflow 2.9 |
| Processamento | Apache Spark 3.5.1 |
| Data Lake | MinIO (S3 compatible) |
| Formato de tabelas | Delta Lake |
| Dashboard | Apache Superset |
| Containerizacao | Docker Compose |

## Fonte de Dados

Dataset de Food Delivery (Kaggle):
- https://www.kaggle.com/datasets/varshinipallerla/food-delivery
- https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset/data

## Como Subir o Ambiente

### Pre-requisitos

- Docker e Docker Compose instalados

### Passo 1 - Clonar o repositorio

```bash
git clone https://github.com/joojpereira/TrbFinalEngenhariaDados.git
cd TrbFinalEngenhariaDados
```

### Passo 2 - Configurar variaveis de ambiente

```bash
cp .env.example .env
```

### Passo 3 - Subir os containers

```bash
docker compose --env-file .env up -d
```

### Passo 4 - Criar usuario do Airflow

```bash
docker exec -it airflow-webserver airflow users create \
  --username admin \
  --password admin123 \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@admin.com
```

### Passo 5 - Inicializar o Superset

```bash
docker exec -it superset superset db upgrade
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@admin.com \
  --password admin123
docker exec -it superset superset init
```

### Passo 6 - Criar os buckets no MinIO

Acesse http://localhost:9001 (minioadmin / minioadmin123) e crie:
- landing
- bronze
- silver
- gold

## Servicos e Portas

| Servico | URL | Usuario | Senha |
|---|---|---|---|
| Airflow | http://localhost:8080 | admin | admin123 |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin123 |
| MinIO API | http://localhost:9000 | minioadmin | minioadmin123 |
| Spark Master UI | http://localhost:8081 | - | - |
| Spark Worker UI | http://localhost:8082 | - | - |
| Superset | http://localhost:8088 | admin | admin123 |
| PostgreSQL | localhost:5432 | admin | admin123 |

## Estrutura do Projeto

TrbFinalEngenhariaDados/
├── dags/                  # DAGs do Airflow
├── data/                  # Dados auxiliares (CSVs originais)
├── docs/                  # Documentacao MkDocs
├── logs/                  # Logs do Airflow
├── plugins/               # Plugins do Airflow
├── docker-compose.yml
├── .env.example
├── mkdocs.yml
└── README.md
## Status do Projeto

- [x] Issue 1 - Infraestrutura Docker Compose
- [ ] Issue 2 - Geracao/carga dos dados de origem
- [ ] Issue 3 - Ingestao Landing Zone
- [ ] Issue 4 - Camada Bronze (Delta Lake)
- [ ] Issue 5 - Camada Silver
- [ ] Issue 6 - Camada Gold (Modelo Dimensional)
- [ ] Issue 7 - Dashboard Superset
- [ ] Issue 8 - Documentacao MkDocs
