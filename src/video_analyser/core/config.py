"""Загрузка конфигов из YAML и переменных окружения."""

from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки из .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_dir: Path = Path("./data")
    config_dir: Path = Path("./configs")
    prompts_dir: Path = Path("./prompts")
    schemas_dir: Path = Path("./schemas")

    asr_model: str = "large-v3"
    asr_device: str = "cpu"
    asr_compute_type: str = "int8"
    asr_language: str = "ru"

    llm_api_url: str = "http://127.0.0.1:10000/v1/chat/completions"
    llm_api_key: str = "12345"
    llm_model: str = "llama"

    cv_device: str = "cpu"

    log_level: str = "INFO"


settings = Settings()


def load_yaml(path: Path) -> dict[str, Any]:
    """Читает YAML-файл и возвращает словарь."""
    if not path.exists():
        raise FileNotFoundError(f"Конфиг не найден: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_rules_dir(rules_dir: Path) -> dict[str, list[dict]]:
    """Загружает все YAML-файлы правил из папки.

    Возвращает словарь {имя_файла: список_правил}.
    """
    result: dict[str, list[dict]] = {}
    for yaml_file in sorted(rules_dir.glob("*.yaml")):
        if yaml_file.name == "severity.yaml":
            continue
        data = load_yaml(yaml_file)
        rules = data.get("rules", [])
        result[yaml_file.stem] = rules
    return result


def load_severity(rules_dir: Path) -> dict[str, list[str]]:
    """Загружает severity.yaml — какие правила critical, какие minor."""
    path = rules_dir / "severity.yaml"
    data = load_yaml(path)
    return {
        "critical": data.get("critical", []),
        "minor": data.get("minor", []),
    }


def load_employees(config_dir: Path) -> list[dict]:
    """Загружает справочник сотрудников."""
    path = config_dir / "employees.yaml"
    if not path.exists():
        return []
    data = load_yaml(path)
    return data.get("employees", [])