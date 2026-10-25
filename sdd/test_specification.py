"""Автоматизированные тесты по спецификации статусов видео (таблица примеров)."""
import pytest

from catalog import Catalog, PlaybackError

# Видео | статус до | действие | ожидаемый статус | ожидаемое сообщение об ошибке
STATUS_EXAMPLES = [
    ("Введение в Python",   "доступно",        "play",   "воспроизводится", None),
    ("Введение в Python",   "воспроизводится", "pause",  "на паузе",        None),
    ("Введение в Python",   "на паузе",        "play",   "воспроизводится", None),
    ("Основы тестирования", "воспроизводится", "finish", "просмотрено",     None),
    ("Основы тестирования", "просмотрено",     "play",   "воспроизводится", None),
    ("Закрытый вебинар",    "недоступно",      "play",   "недоступно",      "Видео недоступно"),
    ("Введение в Python",   "доступно",        "pause",  "доступно",        "Видео не воспроизводится"),
]

# Запрос | ожидаемые заголовки
SEARCH_EXAMPLES = [
    ("python", ["Введение в Python", "Python для анализа данных"]),
    ("ОСНОВЫ", ["Основы тестирования"]),
    ("вебинар", ["Закрытый вебинар"]),
    ("Java", []),
]


@pytest.fixture
def catalog():
    return Catalog([
        ("Введение в Python", "доступно"),
        ("Основы тестирования", "доступно"),
        ("Python для анализа данных", "доступно"),
        ("Закрытый вебинар", "недоступно"),
    ])


@pytest.mark.parametrize(
    "title, before, action, after, error", STATUS_EXAMPLES,
    ids=[f"S{i}" for i in range(1, len(STATUS_EXAMPLES) + 1)],
)
def test_status_transition(catalog, title, before, action, after, error):
    catalog.set_status(title, before)
    if error:
        with pytest.raises(PlaybackError, match=error):
            catalog.apply(title, action)
    else:
        catalog.apply(title, action)
    assert catalog.status(title) == after


@pytest.mark.parametrize(
    "query, expected", SEARCH_EXAMPLES,
    ids=[f"Q{i}" for i in range(1, len(SEARCH_EXAMPLES) + 1)],
)
def test_search_by_title(catalog, query, expected):
    assert catalog.search(query) == expected


def test_only_one_video_plays_at_a_time(catalog):
    catalog.apply("Введение в Python", "play")
    catalog.apply("Основы тестирования", "play")
    assert catalog.status("Введение в Python") == "на паузе"
    assert catalog.status("Основы тестирования") == "воспроизводится"


def test_replay_of_watched_video_starts_from_beginning(catalog):
    catalog.apply("Основы тестирования", "play")
    catalog.apply("Основы тестирования", "finish")
    catalog.apply("Основы тестирования", "play")
    assert catalog.position("Основы тестирования") == 0
