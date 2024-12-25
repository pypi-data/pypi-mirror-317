from dataclasses import dataclass, field

from langcodes import Language


@dataclass()
class Conjugation:
    present: str | None = None
    past: str | None = None
    negative: str | None = None
    te_form: str | None = None
    potential: str | None = None
    polite: str | None = None


@dataclass
class JapaneseReading:
    hiragana: str | None = None
    katakana: str | None = None
    kunyomi: str | None = None
    onyomi: str | None = None


@dataclass
class Forms:
    past_tense: str | None = None
    present_participle: str | None = None
    past_participle: str | None = None
    third_person_singular: str | None = None
    singular: str | None = None
    plural: str | None = None
    comparative: str | None = None
    superlative: str | None = None


@dataclass
class Word:
    word: str
    native_language: Language
    word_language: Language
    native_language_definition: str
    source: str

    example_sentences: list[str] = field(default_factory=list)

    # English properties
    lemma: str | None = None
    forms: Forms | None = None
    pronunciation: str | None = None

    # Japanese properties
    reading: JapaneseReading | None = None
    conjugation: Conjugation | None = None
