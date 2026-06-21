# Arquitetura Medalhão

O pipeline segue a arquitetura Medalhão, separando os dados em diferentes camadas.

## Landing

Armazena os dados brutos no formato original.

## Bronze

Responsável pela conversão dos dados para Delta Lake.

## Silver

Camada destinada à limpeza, padronização e enriquecimento dos dados.

## Gold

Disponibiliza os dados em modelo dimensional para consumo analítico.