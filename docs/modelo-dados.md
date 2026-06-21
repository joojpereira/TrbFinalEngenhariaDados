# Modelo de Dados

## Base Northwind

O projeto utiliza a base Northwind como origem dos dados.

### Principais tabelas

- Customers
- Orders
- Order Details
- Products
- Employees
- Suppliers
- Categories
- Shippers
- Regions
- Territories

## Modelo Dimensional

Fato:
- Pedidos

Dimensões:
- Cliente
- Produto
- Funcionário
- Transportadora
- Região

## Relacionamentos

Orders
 ├── Customer
 ├── Employee
 └── Order Details
        └── Product