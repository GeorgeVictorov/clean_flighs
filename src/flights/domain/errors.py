class ApplicationError(Exception):
    """Base error for the application."""
    ...


class DomainError(ApplicationError):
    """Business rule violation."""
    ...


class InfrastructureError(ApplicationError):
    """Infrastructure failure."""
    ...


class FlightClosed(DomainError): ...


class FlightDeparted(DomainError): ...


class FlightNotFound(DomainError): ...


class SeatDoesNotExist(DomainError): ...


class PassengerAlreadyRegistered(DomainError): ...


class NotReservationOwner(DomainError): ...


class ConflictError(DomainError):
    """Various conflict errors."""
    ...


class SeatAlreadyReserved(ConflictError): ...


class FlightAlreadyExists(ConflictError): ...


class ConcurrencyError(ConflictError): ...
