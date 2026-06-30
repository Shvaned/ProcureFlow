from typing import Any
from pydantic import BaseModel


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any] = {}
    required_permissions: list[str] = []
    business_domain: str = "general"
    version: str = "1.0"


class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = {}


class BaseTool:
    definition: ToolDefinition

    async def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError
