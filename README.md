# Trabalho Final - Engenharia de Dados

## Integrantes

* João Vitor Pereira
* Nome Integrante 2
* Nome Integrante 3

---

# Visão Geral

Este projeto foi desenvolvido para a disciplina de Engenharia de Dados com o objetivo de construir um pipeline de dados completo, contemplando as etapas de geração, armazenamento e processamento de dados.

A base utilizada foi inspirada no banco Northwind. A partir dos dados originais, foram gerados dados sintéticos utilizando Python e Faker para aumentar o volume de registros e simular um ambiente real de vendas.

---

# Tecnologias Utilizadas

* Python 3.13
* Faker
* Pandas
* PostgreSQL
* Docker
* Docker Compose
* Apache Spark
* Git
* GitHub

---

# Arquitetura do Projeto

```text
Dados Originais (Northwind)
            │
            ▼
      Python + Faker
   (Geração dos Dados)
            │
            ▼
        PostgreSQL
     (Armazenamento)
            │
            ▼
       Apache Spark
      (Processamento)
            │
            ▼
      Análise dos Dados
```

---

# Estrutura do Repositório

```text
TrbFinalEngenhariaDados/
│
├── Data/
│   ├── original/
│   │   ├── northwind_orders.csv
│   │   └── northwind_order_details.csv
│   │
│   └── generated/
│       ├── categories.csv
│       ├── customers.csv
│       ├── employees.csv
│       ├── orders.csv
│       ├── order_details.csv
│       ├── products.csv
│       ├── regions.csv
│       ├── shippers.csv
│       ├── suppliers.csv
│       └── territories.csv
│
├── scripts/
│   └── generate_data.py
│
├── requirements.txt
│
└── README.md
```

---

# Base de Dados Original

Dataset utilizado como referência:

https://www.kaggle.com/datasets/emmanueltugbeh/northwind-orders-and-order-details

Arquivos originais:

* northwind_orders.csv
* northwind_order_details.csv

Os arquivos encontram-se na pasta:

```text
Data/original/
```

---

# Geração dos Dados Sintéticos

Para gerar novamente os dados:

```bash
pip install -r requirements.txt

python scripts/generate_data.py
```

Os arquivos serão criados automaticamente em:

```text
Data/generated/
```

O repositório já contém uma versão dos dados gerados, permitindo que o projeto seja executado sem necessidade de nova geração.

---

# Volume de Dados Gerados

| Tabela        | Registros |
| ------------- | --------: |
| customers     |    10.000 |
| products      |    10.000 |
| orders        |    50.000 |
| order_details |   200.000 |
| employees     |       500 |
| suppliers     |     2.000 |
| categories    |       100 |
| shippers      |        20 |
| regions       |        50 |
| territories   |       500 |

**Total aproximado: 273.170 registros**

---

# Características da Base

* Mais de 270 mil registros
* 10 tabelas relacionais
* Dados sintéticos gerados com Faker
* Datas distribuídas nos últimos 3 anos
* Estrutura inspirada no modelo Northwind
* Dados preparados para carga em PostgreSQL

---

# Utilização no PostgreSQL

Os arquivos CSV podem ser importados para PostgreSQL utilizando ferramentas como DBeaver ou pgAdmin.

Ordem recomendada de importação:

1. customers
2. products
3. employees
4. suppliers
5. categories
6. regions
7. shippers
8. territories
9. orders
10. order_details

---

# Controle de Versão

O desenvolvimento do projeto utiliza Git e GitHub para gerenciamento de versões.

Estrutura de branches:

* main → versão estável
* feature/* → desenvolvimento de funcionalidades

As alterações são integradas através de Pull Requests.

---

# Objetivo Final

Disponibilizar uma base de dados em larga escala para testes e estudos de Engenharia de Dados, permitindo a realização de processos de ingestão, armazenamento, transformação e análise de dados utilizando tecnologias modernas do ecossistema de dados.
