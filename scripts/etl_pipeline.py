import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(database_url)

# Locate CSV files
data_dir = Path(__file__).resolve().parent.parent / "data"

# Load in dependency order to satisfy foreign keys
datasets = {
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
}

for table_name, filename in datasets.items():
    print(f"Loading {table_name}...")

    # EXTRACT
    df = pd.read_csv(data_dir / filename)

    # TRANSFORM
    df = df.drop_duplicates()

    # Convert blank strings to NULL
    df = df.replace(r"^\s*$", None, regex=True)

    # LOAD
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    print(f"Loaded {len(df):,} rows into {table_name}")

print("ETL pipeline completed!")