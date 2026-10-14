"""Кастомные исключения проекта."""


class VideoAnalyserError(Exception):
    """Базовое исключение."""


class ConfigError(VideoAnalyserError):
    """Ошибка в конфиге."""


class IngestError(VideoAnalyserError):
    """Ошибка на этапе приёма видео/метаданных."""


class ASRError(VideoAnalyserError):
    """Ошибка распознавания речи."""


class LLMError(VideoAnalyserError):
    """Ошибка вызова LLM."""


class RulesError(VideoAnalyserError):
    """Ошибка в rules engine."""