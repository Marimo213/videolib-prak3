from dataclasses import dataclass


class VideoNotFoundError(Exception):
    """Видео с указанным идентификатором отсутствует в библиотеке."""


@dataclass(frozen=True)
class Video:
    id: int
    title: str
    duration: int  # длительность в секундах


class VideoLibrary:
    def __init__(self, videos):
        self._videos = {video.id: video for video in videos}
        self.now_playing = None
        self.position = 0

    def list_videos(self):
        return list(self._videos.values())

    def search(self, query):
        needle = query.strip().casefold()
        if not needle:
            raise ValueError("Пустой поисковый запрос")
        return [v for v in self._videos.values() if needle in v.title.casefold()]

    def play(self, video_id):
        if video_id not in self._videos:
            raise VideoNotFoundError(video_id)
        self.now_playing = self._videos[video_id]
        self.position = 0
