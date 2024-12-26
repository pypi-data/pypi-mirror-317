from .base import DictionaryBase
from .factory import DictionaryFactory
from .gemini import GeminiDictionary
from .word import Word, Forms, Conjugation, JapaneseReading


__all__ = [
    "DictionaryBase",
    "DictionaryFactory",
    "GeminiDictionary",
    "Word",
    "Forms",
    "Conjugation",
    "JapaneseReading",
]
