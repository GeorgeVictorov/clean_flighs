from psycopg_pool import ConnectionPool

from flights.infrastructure.repo.postgres.postgres_repo import \
    PostgresRepository
from flights.service_layer.uow import AbstractUnitOfWork


class PostgresUnitOfWork(AbstractUnitOfWork):

    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    def __enter__(self):
        self.conn = self._pool.getconn()

        self.flights = PostgresRepository(self.conn)

        return super().__enter__()

    def commit(self):
        self.flights.flush()  # noqa
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __exit__(self, *args):
        try:
            super().__exit__(*args)
        finally:
            self._pool.putconn(self.conn)
