from typing import Any, Optional
from app.core.abstractions import CacheProvider, StorageProvider, EmailProvider


class MockCacheProvider(CacheProvider):
    def __init__(self):
        self._store: dict[str, Any] = {}

    async def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        self._store[key] = value

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def exists(self, key: str) -> bool:
        return key in self._store

    async def clear(self) -> None:
        self._store.clear()


class MockStorageProvider(StorageProvider):
    async def upload(self, file_path: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        return file_path

    async def download(self, file_path: str) -> Optional[bytes]:
        return b"mock_content"

    async def delete(self, file_path: str) -> bool:
        return True

    async def exists(self, file_path: str) -> bool:
        return True

    async def get_url(self, file_path: str, expiry_seconds: int = 3600) -> str:
        return f"/mock/{file_path}"


class MockEmailProvider(EmailProvider):
    def __init__(self):
        self.sent_emails: list[dict] = []

    async def send(self, to: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        self.sent_emails.append({"to": to, "subject": subject, "body": body})
        return True
