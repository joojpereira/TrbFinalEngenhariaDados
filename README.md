# Trabalho Final - Engenharia de Dados

## 📖 Sobre o Projeto

Este projeto tem como objetivo construir um pipeline completo de Engenharia de Dados, realizando a ingestão, transformação, armazenamento e disponibilização de dados para análise através de um dashboard.

O pipeline segue a arquitetura Medalhão (Landing, Bronze, Silver e Gold), utilizando ferramentas modernas do ecossistema de dados.

## 🎯 Objetivos

- Construir um pipeline de dados completo
- Realizar ingestão de dados de uma base relacional
- Armazenar os dados em um Data Lake
- Transformar os dados utilizando Apache Spark
- Disponibilizar um modelo dimensional para consumo
- Criar um dashboard com KPIs e métricas

## 📂 Estrutura Inicial

```
TrbFinalEngenhariaDados/
│
├── Data/
│   ├── northwind_orders.csv
│   └── northwind_order_details.csv
│
└── README.md
```

## 🏗️ Arquitetura do Pipeline

O projeto será organizado seguindo a arquitetura Medalhão, separando os dados em camadas conforme o nível de tratamento e refinamento.

```text
Origem dos Dados
        │
        ▼
Landing - Dados brutos em CSV
        │
        ▼
Bronze - Dados em Delta Lake
        │
        ▼
Silver - Dados tratados e refinados
        │
        ▼
Gold - Modelo dimensional ou OBT
        │
        ▼
Dashboard - KPIs e métricas
```

### Camadas

- **Landing:** armazena os dados brutos no formato original.
- **Bronze:** recebe os dados da Landing e grava em formato Delta Lake.
- **Silver:** contém dados tratados, padronizados e preparados para análise.
- **Gold:** disponibiliza os dados em modelo dimensional ou OBT para consumo no dashboard.

## 🛠️ Tecnologias Utilizadas

Este projeto utiliza as seguintes tecnologias:

| Tecnologia | Finalidade |
|------------|------------|
| Python | Linguagem principal do projeto |
| Apache Spark (PySpark) | Transformação dos dados |
| Apache Airflow | Orquestração do pipeline |
| PostgreSQL | Base de dados de origem |
| Docker | Containerização dos serviços |
| Delta Lake | Armazenamento das camadas Bronze, Silver e Gold |
| Apache Superset | Construção do dashboard |
| MkDocs | Documentação do projeto |
| GitHub | Versionamento e colaboração |

## 📊 Fluxo Geral

```text
PostgreSQL
     │
     ▼
Airflow
     │
     ▼
Landing (CSV)
     │
     ▼
Bronze (Delta)
     │
     ▼
Silver (Delta)
     │
     ▼
Gold (Modelo Dimensional)
     │
     ▼
Superset Dashboard
```

## 🚀 Como executar o projeto

### Pré-requisitos

Antes de iniciar, é necessário possuir as seguintes ferramentas instaladas:

- Docker
- Docker Compose
- Python 3.11+
- Git

### Clonando o repositório

```bash
git clone https://github.com/joojpereira/TrbFinalEngenhariaDados.git
cd TrbFinalEngenhariaDados
```

### Estrutura do Pipeline

O projeto será dividido nas seguintes etapas:

1. Ingestão dos dados de origem
2. Armazenamento na camada Landing
3. Conversão para Delta Lake (Bronze)
4. Tratamento e padronização (Silver)
5. Modelagem dimensional (Gold)
6. Construção do Dashboard

### Documentação

Toda a documentação será disponibilizada através do MkDocs e publicada no GitHub Pages.

## 📁 Organização do Projeto

```
TrbFinalEngenhariaDados/
│
├── Data/
├── docs/
├── dags/
├── scripts/
├── docker/
├── README.md
└── mkdocs.yml
```

Cada diretório possui uma responsabilidade específica para facilitar a manutenção e evolução do projeto.

## 👥 Equipe

Projeto desenvolvido para a disciplina de Engenharia de Dados.

Contribuições realizadas através de GitHub Issues, Pull Requests e revisão de código, seguindo boas práticas de desenvolvimento colaborativo.