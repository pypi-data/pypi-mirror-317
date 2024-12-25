import uuid
from dataclasses import dataclass, field

from langcodes import Language

from verbia_core.dictionary import Forms, JapaneseReading, Conjugation, Word
from verbia_core.utils import time_provider


@dataclass
class Entry:
    vocabulary_id: str
    word: str
    native_language: Language
    native_language_definition: str
    source: str
    is_new: bool
    word_language: Language
    example_sentences: list[str] = field(default_factory=list)

    # English properties
    lemma: str | None = None
    forms: Forms | None = None
    pronunciation: str | None = None

    # Japanese properties
    reading: JapaneseReading | None = None
    conjugation: Conjugation | None = None

    notes: list[str] = field(default_factory=list)
    created_at: int = time_provider.time_mills_from_now()
    next_review_at: int = time_provider.time_mills_from_now(interval_days=1)
    review_interval_days: int = 1
    repetitions: int = 0
    quality: int = 0
    ease_factor: float = 2.5
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_word(cls, word: Word, vocabulary_id: str) -> "Entry":
        return cls(
            word=word.word,
            native_language=word.native_language,
            native_language_definition=word.native_language_definition,
            source=word.source,
            is_new=True,
            word_language=word.word_language,
            example_sentences=word.example_sentences,
            lemma=word.lemma,
            forms=word.forms,
            pronunciation=word.pronunciation,
            reading=word.reading,
            conjugation=word.conjugation,
            vocabulary_id=vocabulary_id,
        )
