from faker import Faker
import pandas as pd
import random
import os
from datetime import timedelta

fake = Faker("pt_BR")

os.makedirs("Data/generated", exist_ok=True)

# --------------------
# CUSTOMERS
# --------------------

customers = []

for i in range(1, 10001):
    customers.append({
        "customer_id": i,
        "customer_name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "created_at": fake.date_between(
            start_date="-3y",
            end_date="today"
        )
    })

customers_df = pd.DataFrame(customers)

# --------------------
# PRODUCTS
# --------------------

products = []

for i in range(1, 10001):
    products.append({
        "product_id": i,
        "product_name": fake.word().capitalize(),
        "unit_price": round(
            random.uniform(5, 500),
            2
        )
    })

products_df = pd.DataFrame(products)

# --------------------
# ORDERS
# --------------------

orders = []

for i in range(1, 50001):

    order_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    orders.append({
        "order_id": i,
        "customer_id": random.randint(
            1,
            10000
        ),
        "order_date": order_date,
        "freight": round(
            random.uniform(10, 200),
            2
        )
    })

orders_df = pd.DataFrame(orders)

# --------------------
# ORDER DETAILS
# --------------------

details = []

for _ in range(200000):

    quantity = random.randint(1, 20)

    price = round(
        random.uniform(5, 500),
        2
    )

    details.append({
        "order_id": random.randint(
            1,
            50000
        ),
        "product_id": random.randint(
            1,
            10000
        ),
        "quantity": quantity,
        "unit_price": price,
        "total": round(
            quantity * price,
            2
        )
    })

details_df = pd.DataFrame(details)


employees = []

for i in range(1, 501):
    employees.append({
        "employee_id": i,
        "employee_name": fake.name(),
        "hire_date": fake.date_between(
            start_date="-10y",
            end_date="today"
        )
    })

employees_df = pd.DataFrame(employees)


suppliers = []

for i in range(1, 2001):
    suppliers.append({
        "supplier_id": i,
        "supplier_name": fake.company(),
        "city": fake.city()
    })

suppliers_df = pd.DataFrame(suppliers)

categories = []

for i in range(1, 101):
    categories.append({
        "category_id": i,
        "category_name": f"Categoria {i}"
    })

categories_df = pd.DataFrame(categories)

shippers = []

for i in range(1, 21):
    shippers.append({
        "shipper_id": i,
        "company_name": fake.company()
    })

shippers_df = pd.DataFrame(shippers)

regions = []

for i in range(1, 51):
    regions.append({
        "region_id": i,
        "region_name": f"Regiao {i}"
    })

regions_df = pd.DataFrame(regions)

territories = []

for i in range(1, 501):
    territories.append({
        "territory_id": i,
        "region_id": random.randint(1, 50),
        "territory_name": fake.city()
    })

territories_df = pd.DataFrame(territories)

# --------------------
# EXPORT
# --------------------

customers_df.to_csv(
    "Data/generated/customers.csv",
    index=False
)

products_df.to_csv(
    "Data/generated/products.csv",
    index=False
)

orders_df.to_csv(
    "Data/generated/orders.csv",
    index=False
)

details_df.to_csv(
    "Data/generated/order_details.csv",
    index=False
)
employees_df.to_csv(
    "Data/generated/employees.csv",
    index=False
)

suppliers_df.to_csv(
    "Data/generated/suppliers.csv",
    index=False
)

categories_df.to_csv(
    "Data/generated/categories.csv",
    index=False
)

shippers_df.to_csv(
    "Data/generated/shippers.csv",
    index=False
)

regions_df.to_csv(
    "Data/generated/regions.csv",
    index=False
)

territories_df.to_csv(
    "Data/generated/territories.csv",
    index=False
)

print("Arquivos gerados com sucesso!")