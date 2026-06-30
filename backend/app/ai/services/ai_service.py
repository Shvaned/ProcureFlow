import json
from typing import Any

from pydantic import BaseModel

from app.ai.providers.openrouter import OpenRouterProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIService:
    def __init__(self):
        self.provider = OpenRouterProvider()

    async def generate_structured(
        self,
        system_prompt: str,
        user_message: str,
        output_schema: type[BaseModel],
        model: str | None = None,
        temperature: float = 0.3,
        max_retries: int = 2,
    ) -> BaseModel:
        schema_description = json.dumps(output_schema.model_json_schema())

        full_system = f"""{system_prompt}

You must respond with valid JSON that matches this schema:
{schema_description}

Respond ONLY with the JSON object. Do not include any other text."""

        last_error = None
        for attempt in range(max_retries + 1):
            try:
                result = await self.provider.complete_structured(
                    system_prompt=full_system,
                    user_message=user_message,
                    output_schema={"type": "json_object"},
                    model=model,
                    temperature=temperature,
                )
                return output_schema.model_validate(result)
            except Exception as e:
                last_error = e
                logger.warning(f"AI structured output attempt {attempt + 1} failed: {e}")

        raise ValueError(f"AI failed to generate valid structured output after {max_retries + 1} attempts. Last error: {last_error}")

    async def explain_business_context(
        self,
        context: dict[str, Any],
        question: str,
        model: str | None = None,
    ) -> str:
        system_prompt = """You are a business analyst for ProcureFlow AI, an enterprise procurement and inventory platform.
You explain business data clearly and concisely. Base your answers ONLY on the provided context.
If you don't have enough information, say so honestly. Never invent data."""

        context_str = json.dumps(context, default=str, indent=2)
        user_message = f"""Business Context:
{context_str}

Question: {question}

Provide a clear, concise analysis based on the data above."""

        result = await self.provider.complete(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model=model,
            temperature=0.3,
        )
        return result["choices"][0]["message"]["content"]
