from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load database credentials from .env
load_dotenv()

# Get database connection details
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

# Connect to PostgreSQL
from sqlalchemy.engine import URL

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=user,
    password=password,
    host=host,
    port=int(port),
    database=database,
)

engine = create_engine(database_url)

# Test connection
with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    print("SUCCESS! Connected to PostgreSQL!")
    print(result.fetchone()[0])