"""Abstraction interfaces for cache, storage, email, and background tasks."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheProvider(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]: ...
    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None: ...
    @abstractmethod
    async def delete(self, key: str) -> None: ...
    @abstractmethod
    async def exists(self, key: str) -> bool: ...
    @abstractmethod
    async def clear(self) -> None: ...


class MemoryCache(CacheProvider):
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


class StorageProvider(ABC):
    @abstractmethod
    async def upload(self, file_path: str, content: bytes, content_type: str = "application/octet-stream") -> str: ...
    @abstractmethod
    async def download(self, file_path: str) -> Optional[bytes]: ...
    @abstractmethod
    async def delete(self, file_path: str) -> bool: ...
    @abstractmethod
    async def exists(self, file_path: str) -> bool: ...
    @abstractmethod
    async def get_url(self, file_path: str, expiry_seconds: int = 3600) -> str: ...


class LocalStorageProvider(StorageProvider):
    def __init__(self, base_path: str = "./uploads"):
        import os
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    async def upload(self, file_path: str, content: bytes, content_type: str = "application/octet-stream") -> str:
        import os
        full_path = os.path.join(self.base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(content)
        return file_path

    async def download(self, file_path: str) -> Optional[bytes]:
        import os
        full_path = os.path.join(self.base_path, file_path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, "rb") as f:
            return f.read()

    async def delete(self, file_path: str) -> bool:
        import os
        full_path = os.path.join(self.base_path, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    async def exists(self, file_path: str) -> bool:
        import os
        return os.path.exists(os.path.join(self.base_path, file_path))

    async def get_url(self, file_path: str, expiry_seconds: int = 3600) -> str:
        return f"/uploads/{file_path}"


class EmailProvider(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str, html_body: Optional[str] = None) -> bool: ...


class LoggingEmailProvider(EmailProvider):
    async def send(self, to: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[EMAIL] To: {to}, Subject: {subject}, Body: {body[:200]}...")
        return True


class NotificationProvider(ABC):
    @abstractmethod
    async def send(self, user_id: str, title: str, body: str, notification_type: str, **kwargs) -> bool: ...


class BackgroundTaskScheduler(ABC):
    @abstractmethod
    async def schedule_immediate(self, task: Any, *args, **kwargs) -> str: ...
    @abstractmethod
    async def schedule_delayed(self, task: Any, delay_seconds: int, *args, **kwargs) -> str: ...
    @abstractmethod
    async def schedule_recurring(self, task: Any, interval_seconds: int, *args, **kwargs) -> str: ...
    @abstractmethod
    async def cancel(self, job_id: str) -> bool: ...
