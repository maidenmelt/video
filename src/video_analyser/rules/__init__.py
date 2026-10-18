"""Rules engine: загрузка правил и применение."""

from .engine import RulesEngine
from .loader import load_rules

__all__ = ["RulesEngine", "load_rules"]