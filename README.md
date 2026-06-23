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
Banco de Dados (PostgreSQL)
            │
            ▼
Orquestração (Apache Airflow)
            │
            ▼
Landing (CSV)
            │
            ▼
Bronze (Delta Lake)
            │
            ▼
Silver (Delta Lake)
            │
            ▼
Gold (Modelo Dimensional)
            │
            ▼
Dashboard (Apache Superset)
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

Atualmente o projeto possui a seguinte estrutura:

```text
TrbFinalEngenhariaDados/
│
├── Data/
│   ├── northwind_orders.csv
│   └── northwind_order_details.csv
│
└── README.md
```

A estrutura será expandida conforme o desenvolvimento das próximas etapas do projeto.

## 👥 Equipe

Projeto desenvolvido para a disciplina de Engenharia de Dados.

O desenvolvimento segue um modelo colaborativo baseado em GitHub Issues, Pull Requests e revisão de código, promovendo organização, rastreabilidade das alterações e boas práticas de desenvolvimento em equipe.

## 🤝 Fluxo de Contribuição

O desenvolvimento do projeto segue o seguinte fluxo:

1. Selecionar uma Issue disponível;
2. Criar uma branch específica para a atividade;
3. Implementar as alterações necessárias;
4. Realizar commits pequenos e descritivos;
5. Enviar a branch para o repositório remoto;
6. Abrir um Pull Request;
7. Aguardar revisão e aprovação antes da integração na branch principal.
