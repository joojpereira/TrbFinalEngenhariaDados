import pandas as pd
import random
from faker import Faker
from datetime import datetime
import os

fake = Faker("pt_BR")

os.makedirs("Data/generated", exist_ok=True)

orders = pd.read_csv("Data/northwind_orders.csv")
details = pd.read_csv("Data/northwind_order_details.csv")

TARGET_ORDERS = 10000

new_orders = []

for i in range(TARGET_ORDERS):

    order_date = fake.date_between(
        start_date="-3y",
        end_date="today"
    )

    required_date = fake.date_between(
        start_date=order_date,
        end_date="+30d"
    )

    shipped_date = fake.date_between(
        start_date=order_date,
        end_date=required_date
    )

    new_orders.append({
        "order_id": i + 1,
        "customer_id": fake.bothify(text="?????").upper(),
        "employee_id": random.randint(1, 20),
        "order_date": order_date,
        "required_date": required_date,
        "shipped_date": shipped_date,
        "ship_via": random.randint(1, 5),
        "freight": round(random.uniform(10, 500), 2),
        "ship_name": fake.company(),
        "ship_address": fake.street_address(),
        "ship_city": fake.city(),
        "ship_region": fake.state_abbr(),
        "ship_postal_code": fake.postcode(),
        "ship_country": "Brazil"
    })

orders_df = pd.DataFrame(new_orders)

orders_df.to_csv(
    "Data/generated/orders.csv",
    index=False
)

print("orders.csv gerado")