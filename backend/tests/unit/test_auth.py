import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationException


class TestAuthService:
    def test_login_invalid_email(self):
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        db.execute = AsyncMock(return_value=mock_result)
        service = AuthService(db)
        with pytest.raises(AuthenticationException):
            import asyncio
            asyncio.run(service.login("bad@test.com", "wrong"))
