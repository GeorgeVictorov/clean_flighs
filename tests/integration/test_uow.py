from flights.domain.model import Flight
from flights.infrastructure.uow.sqlite.sqlite_uow import SqliteUnitOfWork


def get_flight_id_from_db(flight_id, sqlite_session_factory):
    with sqlite_session_factory() as db_conn:
        return db_conn.execute(
            """
            select
                flight_id
            from flights
            where
                flight_id = ? 
            """,
            [flight_id],
        ).fetchone()


def test_add_flight(sqlite_session_factory):
    uow = SqliteUnitOfWork(sqlite_session_factory)
    with uow:
        flight = Flight.create_new(
            flight_id="su-104",
            seat_ids=["A1", "A2", "A3", "A4"],
        )
        uow.flights.add(flight)
        uow.commit()

    row = get_flight_id_from_db("su-104", sqlite_session_factory)

    assert row is not None
    assert row[0] == "su-104"


def test_rollback_discards_new_flight(sqlite_session_factory):
    uow = SqliteUnitOfWork(sqlite_session_factory)

    with uow:
        flight = Flight.create_new(
            flight_id="su-104",
            seat_ids=["A1", "A2"],
        )
        uow.flights.add(flight)

    row = get_flight_id_from_db("su-104", sqlite_session_factory)

    assert row is None


def test_get_returns_same_instance(sqlite_session_factory):
    flight = Flight.create_new(
        flight_id="su-104",
        seat_ids=["A1", "A2"],
    )

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        uow.flights.add(flight)
        uow.commit()

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        f1 = uow.flights.get("su-104")
        f2 = uow.flights.get("su-104")

        assert f1 is f2


def test_commit_updates_existing_flight(sqlite_session_factory):
    flight = Flight.create_new(
        flight_id="su-104",
        seat_ids=["A1", "A2"],
    )

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        uow.flights.add(flight)
        uow.commit()

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        flight = uow.flights.get("su-104")
        flight.reserve("passenger-1", "A1")

        uow.commit()

    with sqlite_session_factory() as conn:
        row = conn.execute(
            """
            select 
                passenger_id
            from seats
            where 
                flight_id = ? and 
                seat_id = ?
            """,
            ("su-104", "A1"),
        ).fetchone()

    assert row[0] == "passenger-1"


def test_commit_without_changes(sqlite_session_factory):
    flight = Flight.create_new(
        flight_id="su-104",
        seat_ids=["A1", "A2"],
    )

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        uow.flights.add(flight)
        uow.commit()

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        uow.flights.get("su-104")
        uow.commit()

    with sqlite_session_factory() as conn:
        version = conn.execute(
            """
            select 
                version
            from flights
            where 
                flight_id = ?
            """,
            ("su-104",),
        ).fetchone()[0]

    assert version == 1


def test_rollback_discards_changes(sqlite_session_factory):
    flight = Flight.create_new(
        flight_id="su-104",
        seat_ids=["A1", "A2"],
    )

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        uow.flights.add(flight)
        uow.commit()

    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        flight = uow.flights.get("su-104")
        flight.reserve("passenger-1", "A1")

    with sqlite_session_factory() as conn:
        row = conn.execute(
            """
            select 
                passenger_id
            from seats
            where 
                flight_id = ? and 
                seat_id = ?
            """,
            ("su-104", "A1"),
        ).fetchone()

    assert row[0] is None


def test_get_returns_none_for_unknown_flight(sqlite_session_factory):
    with SqliteUnitOfWork(sqlite_session_factory) as uow:
        flight = uow.flights.get("unknown")

    assert flight is None
