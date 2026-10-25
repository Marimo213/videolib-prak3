from behave import given, then, when

from player import VideoPlayer


@given("в библиотеке есть видео:")
def step_library(context):
    videos = [
        {"id": int(row["id"]), "title": row["title"], "duration": int(row["duration"])}
        for row in context.table
    ]
    context.player = VideoPlayer(videos)
    context.message = None


@given("открыт список видео")
def step_open_list(context):
    context.visible = context.player.list_videos()


@given('воспроизводится видео "{title}"')
def step_already_playing(context, title):
    context.player.select(title)


@when('я выбираю видео "{title}"')
def step_select(context, title):
    context.message = context.player.select(title)


@when('я ищу видео по запросу "{query}"')
def step_search(context, query):
    context.found = context.player.search(query)


@then('видео "{title}" начинает воспроизводиться')
def step_is_playing(context, title):
    assert context.player.state == "playing", context.player.state
    assert context.player.current["title"] == title


@then("позиция воспроизведения равна {seconds:d} секунд")
def step_position(context, seconds):
    assert context.player.position == seconds


@then("в результатах поиска {count:d} видео")
def step_found_count(context, count):
    assert len(context.found) == count, context.found


@then('я вижу сообщение "{text}"')
def step_message(context, text):
    assert context.message == text, context.message


@then("ничего не воспроизводится")
def step_nothing_playing(context):
    assert context.player.state == "stopped"
    assert context.player.current is None
