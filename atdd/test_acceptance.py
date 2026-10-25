"""Приёмочные тесты, согласованные с заказчиком и бизнес-аналитиком.

AC-1. При открытии каталога пользователь видит список всех видео.
AC-2. При выборе видео оно начинает воспроизводиться.
AC-3. При выборе отсутствующего видео выводится сообщение об ошибке.
AC-4. Поиск по заголовку возвращает только подходящие видео.
AC-5. Если по запросу ничего не найдено, выводится сообщение «Ничего не найдено».
"""
import pytest

from api import VideoApi

CATALOG = [
    {"id": 1, "title": "Введение в Python", "duration": 600},
    {"id": 2, "title": "Основы тестирования", "duration": 1200},
    {"id": 3, "title": "Python для анализа данных", "duration": 1800},
]


@pytest.fixture
def client():
    return VideoApi(CATALOG)


def test_ac1_catalog_shows_all_videos(client):
    response = client.request("GET", "/videos")
    assert response.status == 200
    assert [v["title"] for v in response.json["videos"]] == [
        "Введение в Python", "Основы тестирования", "Python для анализа данных",
    ]


def test_ac2_selected_video_starts_playing(client):
    response = client.request("POST", "/videos/2/play")
    assert response.status == 200
    assert response.json["message"] == "Воспроизведение начато"
    assert response.json["now_playing"] == "Основы тестирования"
    assert response.json["state"] == "playing"


def test_ac3_unknown_video_returns_error(client):
    response = client.request("POST", "/videos/42/play")
    assert response.status == 404
    assert response.json["message"] == "Видео не найдено"


def test_ac4_search_by_title(client):
    response = client.request("GET", "/videos?search=python")
    assert response.status == 200
    assert [v["id"] for v in response.json["videos"]] == [1, 3]


def test_ac5_search_without_results(client):
    response = client.request("GET", "/videos?search=Java")
    assert response.status == 200
    assert response.json["videos"] == []
    assert response.json["message"] == "Ничего не найдено"
