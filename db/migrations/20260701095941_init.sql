-- migrate:up

CREATE TABLE flights (
    flight_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    version INTEGER NOT NULL
);

CREATE TABLE seats (
    flight_id TEXT NOT NULL,
    seat_id TEXT NOT NULL,
    passenger_id TEXT,

    PRIMARY KEY (flight_id, seat_id),

    FOREIGN KEY (flight_id)
        REFERENCES flights(flight_id)
        ON DELETE CASCADE
);

-- migrate:down

DROP TABLE seats;
DROP TABLE flights;