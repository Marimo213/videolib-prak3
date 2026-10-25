# Видеобиблиотека: TDD, ATDD, BDD, SDD

Практическая работа № 3, вариант 19 «Видеоплеер/Библиотека видео».

```sh
python -m venv .venv && .venv/bin/pip install -r requirements.txt
(cd tdd  && ../.venv/bin/python -m unittest -v)
(cd atdd && ../.venv/bin/python -m pytest -v)
(cd bdd  && ../.venv/bin/behave)
(cd sdd  && ../.venv/bin/python -m pytest -v)
```

| Каталог | Подход | Инструмент | Код | Тесты |
|---|---|---|---|---|
| tdd  | TDD  | unittest | video_library.py | test_video_library.py |
| atdd | ATDD | pytest   | api.py           | test_acceptance.py |
| bdd  | BDD  | behave (Gherkin, ru) | player.py | features/play_video.feature, features/steps/player_steps.py |
| sdd  | SDD  | pytest (parametrize) | catalog.py | test_specification.py |
