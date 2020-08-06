import sqlalchemy as sqlalchemy_package
from sqlalchemy.sql import select
from sqlalchemy import create_engine, desc, func, case, cast, and_
from sqlalchemy import Table, MetaData, Column, Integer, Float, String, ForeignKey
import config_psql as creds
import pandas as pd

# Set up a connection to the postgres server
DATABASE_URL = f"postgres://{creds.PGUSER}:{creds.PGPASSWORD}@{creds.PGHOST}:5432/{creds.PGDATABASE}"
engine = sqlalchemy_package.create_engine(DATABASE_URL)
connection = engine.connect()
# employees = pd.read_sql('employees', engine)
# print(employees.head())
