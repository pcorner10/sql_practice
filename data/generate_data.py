"""
generate_data.py
----------------
Generates synthetic datasets for SQL window function practice exercises.
Run this script once to populate the data/ directory with CSV files.

Datasets generated:
  - employees.csv   : 50 employees across 6 departments
  - sales.csv       : ~250 sales records over 2 years (2022-2023)
  - products.csv    : 20 products across 5 categories
  - orders.csv      : ~300 customer orders

Usage:
    python data/generate_data.py
"""

import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


# ---------------------------------------------------------------------------
# 1. EMPLOYEES
# ---------------------------------------------------------------------------
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Susan", "Richard", "Jessica", "Joseph", "Sarah",
    "Thomas", "Karen", "Charles", "Lisa", "Christopher", "Nancy", "Daniel", "Betty",
    "Matthew", "Margaret", "Anthony", "Sandra", "Mark", "Ashley",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin",
]
CITIES = [
    "New York", "Chicago", "Los Angeles", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin",
]

DEPT_CONFIG = {
    "Engineering": {
        "headcount": 15,
        "salary_min": 85_000,
        "salary_max": 210_000,
        "titles": [
            "Junior Engineer", "Engineer", "Senior Engineer",
            "Staff Engineer", "Principal Engineer",
        ],
    },
    "Sales": {
        "headcount": 12,
        "salary_min": 45_000,
        "salary_max": 130_000,
        "titles": [
            "Sales Representative", "Senior Sales Rep",
            "Account Executive", "Sales Manager",
        ],
    },
    "Marketing": {
        "headcount": 8,
        "salary_min": 52_000,
        "salary_max": 125_000,
        "titles": [
            "Marketing Analyst", "Senior Marketing Analyst",
            "Marketing Manager", "Director of Marketing",
        ],
    },
    "Finance": {
        "headcount": 6,
        "salary_min": 72_000,
        "salary_max": 165_000,
        "titles": [
            "Financial Analyst", "Senior Financial Analyst",
            "Finance Manager", "CFO",
        ],
    },
    "HR": {
        "headcount": 5,
        "salary_min": 48_000,
        "salary_max": 105_000,
        "titles": ["HR Coordinator", "HR Specialist", "HR Manager"],
    },
    "Operations": {
        "headcount": 4,
        "salary_min": 58_000,
        "salary_max": 140_000,
        "titles": [
            "Operations Analyst", "Senior Operations Analyst",
            "Operations Manager",
        ],
    },
}

HIRE_START = date(2015, 1, 1)
HIRE_END = date(2023, 12, 31)


def build_employees() -> pd.DataFrame:
    rows = []
    emp_id = 1
    dept_managers: dict = {}
    rng_first = np.random.choice(FIRST_NAMES, 50, replace=True)
    rng_last = np.random.choice(LAST_NAMES, 50, replace=True)
    name_idx = 0

    for dept, cfg in DEPT_CONFIG.items():
        for i in range(cfg["headcount"]):
            fname = rng_first[name_idx]
            lname = rng_last[name_idx]
            name_idx += 1
            title = cfg["titles"][min(i, len(cfg["titles"]) - 1)]
            salary = int(np.random.randint(cfg["salary_min"], cfg["salary_max"]))
            hire_dt = random_date(HIRE_START, HIRE_END)
            manager_id = None if i == 0 else dept_managers[dept]
            if i == 0:
                dept_managers[dept] = emp_id

            rows.append(
                {
                    "employee_id": emp_id,
                    "first_name": fname,
                    "last_name": lname,
                    "full_name": f"{fname} {lname}",
                    "department": dept,
                    "job_title": title,
                    "salary": salary,
                    "hire_date": hire_dt.isoformat(),
                    "manager_id": manager_id,
                    "city": random.choice(CITIES),
                }
            )
            emp_id += 1

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. PRODUCTS
# ---------------------------------------------------------------------------
PRODUCT_DATA = [
    # (name, category, unit_price, cost)
    ("Laptop Pro 15", "Electronics", 1_299.99, 780.00),
    ("Wireless Mouse", "Electronics", 29.99, 12.00),
    ("Standing Desk", "Furniture", 499.00, 220.00),
    ("Office Chair", "Furniture", 389.00, 155.00),
    ("Monitor 27in", "Electronics", 349.99, 175.00),
    ("Mechanical Keyboard", "Electronics", 129.99, 55.00),
    ("Noise Cancelling Headphones", "Electronics", 249.99, 110.00),
    ("Webcam HD", "Electronics", 89.99, 35.00),
    ("Whiteboard XL", "Office Supplies", 75.00, 28.00),
    ("Printer All-in-One", "Electronics", 199.99, 90.00),
    ("Desk Lamp LED", "Furniture", 39.99, 14.00),
    ("Notebook Pack (10)", "Office Supplies", 14.99, 5.00),
    ("Pen Set Premium", "Office Supplies", 12.99, 4.00),
    ("Ergonomic Mouse Pad", "Office Supplies", 24.99, 9.00),
    ("USB-C Hub 7-port", "Electronics", 59.99, 22.00),
    ("Cloud Storage 1TB/yr", "Software", 99.99, 10.00),
    ("Project Mgmt License", "Software", 149.99, 15.00),
    ("Antivirus Suite", "Software", 49.99, 5.00),
    ("Video Conf License", "Software", 199.99, 20.00),
    ("Data Analytics Suite", "Software", 299.99, 30.00),
]


def build_products() -> pd.DataFrame:
    rows = []
    for i, (name, category, price, cost) in enumerate(PRODUCT_DATA, start=1):
        rows.append(
            {
                "product_id": i,
                "product_name": name,
                "category": category,
                "unit_price": price,
                "cost": cost,
                "margin_pct": round((price - cost) / price * 100, 1),
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 3. SALES (sales rep performance records)
# ---------------------------------------------------------------------------
REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
CATEGORIES_SALES = ["Software", "Hardware", "Services", "Training", "Support"]


def build_sales(employees: pd.DataFrame) -> pd.DataFrame:
    sales_reps = employees[employees["department"] == "Sales"].copy()
    rows = []
    sale_id = 1
    sale_start = date(2022, 1, 1)
    sale_end = date(2023, 12, 31)

    for _, rep in sales_reps.iterrows():
        n_sales = random.randint(18, 28)
        region = random.choice(REGIONS)
        for _ in range(n_sales):
            sale_dt = random_date(sale_start, sale_end)
            amount = round(random.uniform(2_000, 85_000), 2)
            category = random.choice(CATEGORIES_SALES)
            rows.append(
                {
                    "sale_id": sale_id,
                    "rep_id": int(rep["employee_id"]),
                    "rep_name": rep["full_name"],
                    "region": region,
                    "category": category,
                    "amount": amount,
                    "sale_date": sale_dt.isoformat(),
                    "year": sale_dt.year,
                    "quarter": f"Q{(sale_dt.month - 1) // 3 + 1}",
                    "month": sale_dt.month,
                    "month_label": sale_dt.strftime("%Y-%m"),
                }
            )
            sale_id += 1

    df = pd.DataFrame(rows)
    df = df.sort_values("sale_date").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# 4. ORDERS (customer orders)
# ---------------------------------------------------------------------------
CUSTOMER_NAMES = [
    "Acme Corp", "Globex Inc", "Initech", "Umbrella Corp", "Hooli",
    "Pied Piper", "Dunder Mifflin", "Bluth Company", "Sterling Cooper",
    "Vandelay Industries", "Prestige Worldwide", "Monarch Corporation",
    "Oceanic Airlines", "Waystar Royco", "Cyberdyne Systems",
]


def build_orders(products: pd.DataFrame) -> pd.DataFrame:
    rows = []
    order_id = 1
    ord_start = date(2022, 1, 1)
    ord_end = date(2023, 12, 31)
    customer_ids = list(range(1, len(CUSTOMER_NAMES) + 1))

    for _ in range(300):
        prod = products.sample(1).iloc[0]
        cust_id = random.choice(customer_ids)
        cust_nm = CUSTOMER_NAMES[cust_id - 1]
        qty = random.randint(1, 20)
        price = prod["unit_price"]
        total = round(price * qty, 2)
        ord_dt = random_date(ord_start, ord_end)

        rows.append(
            {
                "order_id": order_id,
                "customer_id": cust_id,
                "customer_name": cust_nm,
                "product_id": int(prod["product_id"]),
                "product_name": prod["product_name"],
                "category": prod["category"],
                "order_date": ord_dt.isoformat(),
                "year": ord_dt.year,
                "quarter": f"Q{(ord_dt.month - 1) // 3 + 1}",
                "month": ord_dt.month,
                "month_label": ord_dt.strftime("%Y-%m"),
                "quantity": qty,
                "unit_price": price,
                "total_amount": total,
                "region": random.choice(REGIONS),
            }
        )
        order_id += 1

    df = pd.DataFrame(rows)
    df = df.sort_values("order_date").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Generating datasets...")

    employees = build_employees()
    products = build_products()
    sales = build_sales(employees)
    orders = build_orders(products)

    employees.to_csv(os.path.join(OUTPUT_DIR, "employees.csv"), index=False)
    products.to_csv(os.path.join(OUTPUT_DIR, "products.csv"), index=False)
    sales.to_csv(os.path.join(OUTPUT_DIR, "sales.csv"), index=False)
    orders.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False)

    print(f"  employees : {len(employees):>4} rows  -> {OUTPUT_DIR}/employees.csv")
    print(f"  products  : {len(products):>4} rows  -> {OUTPUT_DIR}/products.csv")
    print(f"  sales     : {len(sales):>4} rows  -> {OUTPUT_DIR}/sales.csv")
    print(f"  orders    : {len(orders):>4} rows  -> {OUTPUT_DIR}/orders.csv")
    print("Done.")


if __name__ == "__main__":
    main()
