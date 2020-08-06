from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
import pandas as pd

engine = create_engine('sqlite:///demo.db')
Base = declarative_base()

# Set up a connection to the postgres server
DATABASE_URL = f"postgres://{creds.PGUSER}:{creds.PGPASSWORD}@{creds.PGHOST}:5432/{creds.PGDATABASE}"
engine = sqlalchemy_package.create_engine(DATABASE_URL)
connection = engine.connect()
