"""Логика определения критичности правил."""

from pathlib import Path

from video_analyser.core.config import load_yaml


class SeverityMap:
    """Справочник: какие правила critical, какие minor."""

    def __init__(self, critical: list[str], minor: list[str]) -> None:
        self.critical = set(critical)
        self.minor = set(minor)

    def get(self, rule_id: str) -> str:
        """Возвращает severity для правила. Если не найдено — считаем critical."""
        if rule_id in self.critical:
            return "critical"
        if rule_id in self.minor:
            return "minor"
        return "critical"

    @classmethod
    def from_file(cls, path: Path) -> "SeverityMap":
        """Загружает из severity.yaml."""
        data = load_yaml(path)
        return cls(
            critical=data.get("critical", []),
            minor=data.get("minor", []),
        )