# Pipeline de Dados

## Fluxo Geral

```text
PostgreSQL
     │
     ▼
Airflow
     │
     ▼
Landing
     │
     ▼
Bronze
     │
     ▼
Silver
     │
     ▼
Gold
     │
     ▼
Dashboard
```

Cada etapa possui uma responsabilidade específica dentro do processo de Engenharia de Dados.