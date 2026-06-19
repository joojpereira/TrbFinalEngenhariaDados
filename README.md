# Trabalho Final - Engenharia de Dados

## Integrantes

* João Vitor Pereira
* Nome Integrante 2
* Nome Integrante 3

---

# Visão Geral

Este projeto tem como objetivo desenvolver um pipeline de Engenharia de Dados completo, contemplando as etapas de geração, ingestão, armazenamento, processamento e análise de dados.

A base utilizada foi inspirada no banco Northwind e expandida por meio da geração de dados sintéticos utilizando Python e Faker, permitindo simular um ambiente real de vendas com grande volume de informações.

---

# Arquitetura do Projeto

```text
Origem dos Dados
        │
        ▼
Python + Faker
(Geração dos CSVs)
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
Camada Analítica
(Relatórios e KPIs)
```

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

# Estrutura do Repositório

```text
TrbFinalEngenhariaDados/
│
├── Data/
│   ├── northwind_orders.csv
│   ├── northwind_order_details.csv
│   └── generated/
│
├── scripts/
│   └── generate_data.py
│
├── requirements.txt
│
└── README.md
```

---

# Fonte de Dados

O projeto utiliza como base os arquivos do conjunto Northwind:

* northwind_orders.csv
* northwind_order_details.csv

A partir destes arquivos foi desenvolvido um gerador de dados sintéticos capaz de ampliar o volume da base para atender aos requisitos do projeto.

---

# Geração de Dados Sintéticos

Os dados são gerados automaticamente utilizando a biblioteca Faker.

Para executar:

```bash
pip install -r requirements.txt

python scripts/generate_data.py
```

Os arquivos gerados são armazenados em:

```text
Data/generated/
```

---

# Tabelas Geradas

| Tabela        | Quantidade de Registros |
| ------------- | ----------------------: |
| customers     |                  10.000 |
| employees     |                     500 |
| suppliers     |                   2.000 |
| categories    |                     100 |
| products      |                  10.000 |
| shippers      |                      20 |
| regions       |                      50 |
| territories   |                     500 |
| orders        |                  50.000 |
| order_details |                 200.000 |

Total aproximado: **272.170 registros**

---

# Características da Base

* Mais de 270 mil registros
* 10 tabelas relacionais
* Dados sintéticos realistas
* Datas distribuídas nos últimos 3 anos
* Simulação de operações de vendas
* Estrutura inspirada no Northwind

---

# Objetivos do Pipeline

O pipeline desenvolvido deverá permitir:

* Ingestão automatizada dos dados
* Armazenamento em banco relacional
* Transformação e enriquecimento dos dados
* Processamento em larga escala
* Geração de indicadores de negócio

---

# Indicadores Esperados

Entre as análises previstas estão:

* Total de vendas por período
* Produtos mais vendidos
* Clientes com maior volume de compras
* Ticket médio por pedido
* Distribuição geográfica das vendas
* Custos de frete
* Evolução temporal das vendas

---

# Controle de Versão

O desenvolvimento segue fluxo baseado em Git Flow simplificado:

* main → versão estável
* feature/* → desenvolvimento de funcionalidades
* Pull Requests → integração das alterações

Todas as modificações passam por revisão antes da integração na branch principal.

---

# Responsabilidades

### Origem dos Dados

* Geração dos dados sintéticos
* Modelagem dos arquivos CSV
* Garantia do volume mínimo de dados

### Infraestrutura

* Docker
* Docker Compose
* Banco de dados

### Processamento

* Apache Spark
* Transformações e agregações

### Análise

* Criação de métricas e indicadores
* Visualização dos resultados

---

# Resultado Esperado

Ao final do projeto será disponibilizado um ambiente completo de Engenharia de Dados capaz de gerar, armazenar, processar e analisar grandes volumes de dados de vendas, simulando um cenário corporativo real.
