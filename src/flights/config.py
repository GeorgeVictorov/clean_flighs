import os


def _build_postgres_uri(db_name: str) -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "abc123")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri() -> str:
    return _build_postgres_uri(os.getenv("POSTGRES_DB", "flights"))


def get_test_postgres_uri() -> str:
    return _build_postgres_uri(os.getenv("POSTGRES_DB_TEST", "flights_test"))
