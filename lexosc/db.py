import os
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row

@contextmanager
def connection():
    dsn = os.getenv('DATABASE_URL', 'postgresql://lexosc:lexosc@localhost:5432/lexosc')
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        yield conn
