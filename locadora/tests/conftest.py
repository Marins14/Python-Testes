import psycopg2
import pytest
import os


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        database=os.getenv("POSTGRES_DB", "locadora"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    cur = conn.cursor()

    cur.execute("""
    CREATE EXTENSION IF NOT EXISTS unaccent;

    CREATE TABLE IF NOT EXISTS filmes (
        id SERIAL PRIMARY KEY,
        titulo TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


@pytest.fixture(autouse=True)
def clean_table(setup_database):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        database=os.getenv("POSTGRES_DB", "locadora"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE filmes RESTART IDENTITY;")
    conn.commit()

    cur.close()
    conn.close()


@pytest.fixture
def insert_data():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        database=os.getenv("POSTGRES_DB", "locadora"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO filmes (titulo, quantidade) VALUES (%s, %s);",
        ("teste", 1)
    )

    conn.commit()
    cur.close()
    conn.close()