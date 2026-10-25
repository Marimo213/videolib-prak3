import unittest

from video_library import Video, VideoLibrary, VideoNotFoundError


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.library = VideoLibrary([
            Video(1, "Введение в Python", 600),
            Video(2, "Python для анализа данных", 1800),
            Video(3, "Основы тестирования", 1200),
        ])

    def test_search_finds_by_part_of_title(self):
        result = self.library.search("python")
        self.assertEqual([v.id for v in result], [1, 2])

    def test_search_ignores_case_and_spaces(self):
        result = self.library.search("  ОСНОВЫ  ")
        self.assertEqual([v.id for v in result], [3])

    def test_search_returns_empty_list_when_nothing_found(self):
        self.assertEqual(self.library.search("Java"), [])

    def test_search_with_empty_query_raises_error(self):
        with self.assertRaises(ValueError):
            self.library.search("   ")


class TestPlay(unittest.TestCase):
    def setUp(self):
        self.library = VideoLibrary([
            Video(1, "Введение в Python", 600),
            Video(2, "Основы тестирования", 1200),
        ])

    def test_play_sets_current_video(self):
        self.library.play(2)
        self.assertEqual(self.library.now_playing.title, "Основы тестирования")

    def test_play_starts_from_beginning(self):
        self.library.play(1)
        self.assertEqual(self.library.position, 0)

    def test_play_unknown_video_raises_error(self):
        with self.assertRaises(VideoNotFoundError):
            self.library.play(99)

    def test_nothing_is_playing_by_default(self):
        self.assertIsNone(self.library.now_playing)


if __name__ == "__main__":
    unittest.main()
