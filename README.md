# 🚀 Trabalho Final - Engenharia de Dados

Pipeline completo de Engenharia de Dados utilizando PostgreSQL, Airflow, MinIO, Apache Spark, Delta Lake, Apache Superset, Docker Compose e MkDocs.

O projeto segue a arquitetura Medalhão, com as camadas:

```text
Landing → Bronze → Silver → Gold → Dashboard
```

---

## 📖 Sobre o Projeto

Este projeto tem como objetivo construir um pipeline de dados completo, realizando a ingestão, transformação, armazenamento e disponibilização dos dados para análise por meio de dashboards.

A solução utiliza um ambiente containerizado com Docker Compose, contendo os principais serviços necessários para a execução do pipeline.

---

## 👥 Equipe

| Integrante |
|-----------|
| Bruno Sabino |
| Filipe Jeremias |
| João Vitor Pereira |
| Nathan Frassetto |
| Rafael Pagnan |
| Ryan Candeu |

---

## 🎯 Objetivos

- Construir um pipeline completo de Engenharia de Dados;
- Utilizar PostgreSQL como base de dados de origem;
- Orquestrar processos com Apache Airflow;
- Armazenar dados em um Data Lake no MinIO;
- Aplicar arquitetura Medalhão;
- Transformar dados utilizando Apache Spark;
- Utilizar Delta Lake nas camadas Bronze, Silver e Gold;
- Disponibilizar dados para análise no Apache Superset;
- Documentar o projeto com README e MkDocs.

---

## 🏗️ Arquitetura Geral

```text
PostgreSQL (Origem)
        │
        ▼
Apache Airflow (Orquestração)
        │
        ▼
MinIO - Landing (CSV bruto)
        │
        ▼
Apache Spark
        │
        ▼
MinIO - Bronze (Delta Lake)
        │
        ▼
Apache Spark
        │
        ▼
MinIO - Silver (Delta Lake)
        │
        ▼
Apache Spark
        │
        ▼
MinIO - Gold (Modelo Dimensional)
        │
        ▼
Apache Superset (Dashboard)
```

---

## 🛠️ Stack Tecnológica

| Camada | Ferramenta |
|---|---|
| Banco de origem | PostgreSQL 15 |
| Orquestração | Apache Airflow 2.9 |
| Data Lake | MinIO |
| Processamento | Apache Spark 3.5.1 |
| Formato de armazenamento | Delta Lake |
| Visualização | Apache Superset |
| Documentação | MkDocs |
| Versionamento | GitHub |
| Ambiente | Docker Compose |

---

## 🏛️ Arquitetura Medalhão

### Landing

Camada responsável por armazenar os dados brutos no formato original.

No projeto, a Landing será armazenada no MinIO em formato CSV.

Exemplo de caminho esperado:

```text
landing/sql/{tabela}/YYYY/MM/DD/arquivo.csv
```

---

### Bronze

Camada responsável por receber os dados da Landing e convertê-los para Delta Lake.

---

### Silver

Camada responsável por limpar, padronizar e refinar os dados.

---

### Gold

Camada final do pipeline, onde os dados serão organizados em modelo dimensional ou OBT para consumo analítico no dashboard.

---

## 📂 Estrutura do Projeto

```text
TrbFinalEngenhariaDados/
│
├── Data/
│   ├── original/
│   └── generated/
│
├── scripts/
│   └── generate_data.py
│
├── docs/
│
├── dags/
│
├── logs/
│
├── plugins/
│
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── mkdocs.yml
└── README.md
```

---

## 🗄️ Dados de Origem

O projeto utiliza uma base baseada no modelo Northwind, com dados originais e dados sintéticos gerados para simulação do ambiente de origem.

As tabelas principais incluem:

- customers
- orders
- order_details
- products
- employees
- suppliers
- categories
- shippers
- regions
- territories

---

## 🚀 Como subir o ambiente

### Pré-requisitos

Antes de iniciar, é necessário possuir:

- Git;
- Docker;
- Docker Compose.

---

### 1. Clonar o repositório

```bash
git clone https://github.com/joojpereira/TrbFinalEngenhariaDados.git
cd TrbFinalEngenhariaDados
```

---

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

---

### 3. Subir os containers

```bash
docker compose --env-file .env up -d
```

---

### 4. Criar usuário do Airflow

Caso o usuário não tenha sido criado automaticamente pelo container `airflow-init`, execute:

```bash
docker exec -it airflow-webserver airflow users create \
  --username admin \
  --password admin123 \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@admin.com
```

---

### 5. Inicializar o Superset

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

---

### 6. Criar buckets no MinIO

Acesse o console do MinIO:

```text
http://localhost:9001
```

Credenciais:

```text
Usuário: minioadmin
Senha: minioadmin123
```

Crie os buckets:

- landing
- bronze
- silver
- gold

---

## 🌐 Serviços e Portas

| Serviço | URL | Usuário | Senha |
|---|---|---|---|
| Airflow | http://localhost:8080 | admin | admin123 |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin123 |
| MinIO API | http://localhost:9000 | minioadmin | minioadmin123 |
| Spark Master UI | http://localhost:8081 | - | - |
| Spark Worker UI | http://localhost:8082 | - | - |
| Superset | http://localhost:8088 | admin | admin123 |
| PostgreSQL | localhost:5432 | admin | admin123 |

---

## 📊 Fluxo do Pipeline

```text
1. PostgreSQL armazena os dados de origem
2. Airflow orquestra as execuções
3. Os dados são extraídos para a camada Landing no MinIO
4. Spark processa os dados para Bronze
5. Spark refina os dados para Silver
6. Spark modela os dados para Gold
7. Superset consome os dados da Gold para dashboards
```

---

## 📚 Documentação MkDocs

A documentação completa do projeto será publicada com MkDocs.

Comandos principais:

```bash
mkdocs serve
```

Visualização local:

```text
http://127.0.0.1:8000
```

Gerar build:

```bash
mkdocs build
```

Publicar no GitHub Pages:

```bash
mkdocs gh-deploy
```

---

## 🤝 Fluxo de Contribuição

O desenvolvimento do projeto segue um fluxo colaborativo baseado em GitHub Issues e Pull Requests.

```text
Issue
  │
  ▼
Branch
  │
  ▼
Commits
  │
  ▼
Push
  │
  ▼
Pull Request
  │
  ▼
Code Review
  │
  ▼
Merge na branch principal
```

Boas práticas:

- Não trabalhar diretamente na branch principal;
- Criar uma branch para cada issue;
- Fazer commits pequenos e descritivos;
- Abrir Pull Request para revisão;
- Aguardar aprovação antes do merge;
- Manter README e MkDocs atualizados.

---

## ✅ Status das Issues

| Issue | Descrição | Status |
|---|---|---|
| #1 | Configurar Docker Compose com todos os serviços | Em desenvolvimento |
| #2 | Carregar esquema Northwind e expandir com Python Faker | Em desenvolvimento |
| #3 | Criar DAG Airflow PostgreSQL → Landing | Pendente |
| #4 | Job PySpark Landing → Bronze | Pendente |
| #5 | Job PySpark Bronze → Silver | Pendente |
| #6 | Job PySpark Silver → Gold | Pendente |
| #7 | Configurar Superset e conectar à Gold | Pendente |
| #8 | Criar dashboard com KPIs e métricas | Pendente |
| #9 | Criar documentação MkDocs | Em desenvolvimento |
| #10 | Finalizar README | Em desenvolvimento |

---

## 📄 Licença

Projeto desenvolvido exclusivamente para fins acadêmicos na disciplina de Engenharia de Dados.