"""Анализатор речи через локальный LLM-сервер (vLLM / Ollama).

Обращается по HTTP к эндпоинту /v1/chat/completions.
Никаких облачных сервисов — всё локально.
"""

import json
from pathlib import Path

import httpx
from loguru import logger

from video_analyser.core.config import settings
from video_analyser.core.exceptions import LLMError


class LLMClient:
    """Клиент для локального LLM. Стиль совпадает с Audio Analyser."""

    def __init__(self) -> None:
        self.api_url = settings.llm_api_url
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.timeout = 180.0

    def analyze(self, prompt: str, text: str, schema: dict | None = None) -> dict:
        """Отправляет текст с промтом и опциональной JSON-схемой.

        Возвращает распарсенный JSON-ответ или {"raw_output": ...} при ошибке парсинга.
        """
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]

        payload: dict = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
            "stream": False,
        }

        if schema is not None:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": schema,
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as e:
            logger.error(f"Ошибка вызова LLM: {e}")
            raise LLMError(f"Не удалось получить ответ от LLM: {e}") from e

        content = data["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("LLM вернул не-JSON, возвращаем raw_output")
            return {"raw_output": content}


def load_prompt(path: Path) -> str:
    """Читает промт из файла."""
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def load_schema(path: Path) -> dict:
    """Читает JSON-схему из файла."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)