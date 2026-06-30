import uuid
from datetime import datetime, timezone
from app.models.identity.user import User
from app.core.security import hash_password


def create_test_user(
    email: str = "test@procureflow.ai",
    name: str = "Test User",
    password: str = "Test@123",
    is_active: bool = True,
) -> User:
    return User(
        id=uuid.uuid4(),
        email=email,
        name=name,
        hashed_password=hash_password(password),
        is_active=is_active,
        is_locked=False,
        failed_login_attempts=0,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_deleted=False,
    )
