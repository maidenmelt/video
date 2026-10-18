"""Общие типы для проекта."""

from typing import Literal

# Роль сотрудника
Role = Literal["admin", "doctor", "coordinator", "auditor"]

# Критичность правила
Severity = Literal["critical", "minor"]

# Тип анализа
AnalysisType = Literal["audio", "video", "metadata", "combined"]

# Итоговый статус
ReportType = Literal["служебная", "ознакомительная", "нет"]