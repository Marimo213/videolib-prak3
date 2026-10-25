class VideoPlayer:
    """Плеер видеобиблиотеки: список, поиск и запуск воспроизведения."""

    def __init__(self, videos):
        self.videos = list(videos)
        self.current = None
        self.position = 0
        self.state = "stopped"

    def list_videos(self):
        return list(self.videos)

    def search(self, query):
        needle = query.strip().casefold()
        return [v for v in self.videos if needle in v["title"].casefold()]

    def select(self, title):
        video = next((v for v in self.videos if v["title"] == title), None)
        if video is None:
            return "Видео не найдено"
        self.current = video
        self.position = 0
        self.state = "playing"
        return f"Воспроизводится: {title}"
