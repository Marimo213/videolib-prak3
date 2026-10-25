AVAILABLE = "доступно"
PLAYING = "воспроизводится"
PAUSED = "на паузе"
WATCHED = "просмотрено"
UNAVAILABLE = "недоступно"


class PlaybackError(Exception):
    pass


class _Entry:
    def __init__(self, title, status, duration):
        self.title = title
        self.status = status
        self.duration = duration
        self.position = 0


class Catalog:
    """Каталог видео со статусами воспроизведения по спецификации SDD."""

    def __init__(self, videos):
        self._entries = {}
        for title, status, *rest in videos:
            duration = rest[0] if rest else 600
            self._entries[title] = _Entry(title, status, duration)

    def _get(self, title):
        try:
            return self._entries[title]
        except KeyError:
            raise PlaybackError("Видео не найдено") from None

    def set_status(self, title, status):
        self._get(title).status = status

    def status(self, title):
        return self._get(title).status

    def position(self, title):
        return self._get(title).position

    def search(self, query):
        needle = query.strip().casefold()
        return [t for t in self._entries if needle in t.casefold()]

    def apply(self, title, action):
        entry = self._get(title)
        handlers = {"play": self._play, "pause": self._pause, "finish": self._finish}
        if action not in handlers:
            raise ValueError(f"Неизвестное действие: {action}")
        handlers[action](entry)

    @staticmethod
    def _require_playing(entry):
        if entry.status != PLAYING:
            raise PlaybackError("Видео не воспроизводится")

    def _pause(self, entry):
        self._require_playing(entry)
        entry.status = PAUSED

    def _finish(self, entry):
        self._require_playing(entry)
        entry.status = WATCHED
        entry.position = entry.duration

    def _play(self, entry):
        if entry.status == UNAVAILABLE:
            raise PlaybackError("Видео недоступно")
        for other in self._entries.values():
            if other is not entry and other.status == PLAYING:
                other.status = PAUSED
        if entry.status in (AVAILABLE, WATCHED):
            entry.position = 0
        entry.status = PLAYING
