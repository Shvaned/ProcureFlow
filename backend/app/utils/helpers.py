import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


def uuid_to_str(value: uuid.UUID) -> str:
    return str(value)


def str_to_uuid(value: str) -> uuid.UUID:
    return uuid.UUID(value)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def today() -> date:
    return date.today()


def safe_decimal(value: Any, default: str = "0") -> Decimal:
    try:
        return Decimal(str(value))
    except (ValueError, TypeError, ArithmeticError):
        return Decimal(default)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def truncate_string(value: str, max_length: int = 500) -> str:
    if len(value) <= max_length:
        return value
    return value[:max_length] + "..."
