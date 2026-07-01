import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    password = os.environ.get("POSTGRES_PASSWORD", "abc123")
    user = os.environ.get("POSTGRES_USER", "postgres")
    db_name = os.environ.get("POSTGRES_DB", "flights")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
