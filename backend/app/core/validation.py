from typing import Any

from pydantic import BaseModel, ValidationError

from app.core.exceptions import ValidationException


class BusinessValidator:
    @staticmethod
    def validate_required(value: Any, field_name: str) -> None:
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationException(f"{field_name} is required")

    @staticmethod
    def validate_positive(value: int | float, field_name: str) -> None:
        if value < 0:
            raise ValidationException(f"{field_name} must be positive")

    @staticmethod
    def validate_min_length(value: str, min_len: int, field_name: str) -> None:
        if len(value) < min_len:
            raise ValidationException(f"{field_name} must be at least {min_len} characters")

    @staticmethod
    def validate_max_length(value: str, max_len: int, field_name: str) -> None:
        if len(value) > max_len:
            raise ValidationException(f"{field_name} must be at most {max_len} characters")

    @staticmethod
    def validate_range(value: int | float, min_val: int | float, max_val: int | float, field_name: str) -> None:
        if value < min_val or value > max_val:
            raise ValidationException(f"{field_name} must be between {min_val} and {max_val}")

    @staticmethod
    def validate_unique(existing: bool, field_name: str) -> None:
        if existing:
            raise ValidationException(f"A record with this {field_name} already exists")

    @staticmethod
    def validate_pydantic(model: BaseModel) -> list[str] | None:
        try:
            model.model_validate(model)
            return None
        except ValidationError as e:
            return [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
