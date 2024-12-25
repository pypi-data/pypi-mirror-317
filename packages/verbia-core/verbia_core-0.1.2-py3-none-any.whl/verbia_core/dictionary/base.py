from abc import ABC, abstractmethod

from langcodes import Language

from verbia_core.dictionary.word import Word


class DictionaryBase(ABC):
    def __init__(self, source: str):
        self._source = source

    @abstractmethod
    def lookup(
        self, word: str, word_language: Language, native_language: Language
    ) -> Word | None:
        pass

    @abstractmethod
    async def async_lookup(
        self, word: str, word_language: Language, native_language: Language
    ) -> Word | None:
        pass
