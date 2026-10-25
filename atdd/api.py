import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlsplit


@dataclass
class Response:
    status: int
    json: dict


class VideoApi:
    """Упрощённый HTTP-интерфейс видеобиблиотеки."""

    PLAY_ROUTE = re.compile(r"^/videos/(\d+)/play$")

    def __init__(self, catalog):
        self.catalog = {video["id"]: video for video in catalog}
        self.now_playing = None

    def request(self, method, path):
        url = urlsplit(path)
        if method == "GET" and url.path == "/videos":
            query = parse_qs(url.query).get("search", [""])[0]
            return self._list(query)
        match = self.PLAY_ROUTE.match(url.path)
        if method == "POST" and match:
            return self._play(int(match.group(1)))
        return Response(404, {"message": "Маршрут не найден"})

    def _list(self, query):
        videos = list(self.catalog.values())
        if query:
            needle = query.strip().casefold()
            videos = [v for v in videos if needle in v["title"].casefold()]
            if not videos:
                return Response(200, {"videos": [], "message": "Ничего не найдено"})
        return Response(200, {"videos": videos})

    def _play(self, video_id):
        video = self.catalog.get(video_id)
        if video is None:
            return Response(404, {"message": "Видео не найдено"})
        self.now_playing = video
        return Response(200, {
            "message": "Воспроизведение начато",
            "now_playing": video["title"],
            "state": "playing",
        })
