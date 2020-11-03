from datetime import datetime
from random import randint

import factory
from dateutil.tz import UTC
from factory import fuzzy
from backend.models.post import Post
from tests.factories.board import BoardFactory
from tests.factories.comment import CommentFactory
from tests.factories.user import UserFactory


class PostFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Post

    title = fuzzy.FuzzyText(length=5)
    board = factory.SubFactory(BoardFactory)
    likes = fuzzy.FuzzyInteger(low=0, high=100)
    content = fuzzy.FuzzyText(length=20)
    writer = factory.SubFactory(UserFactory)
    created = fuzzy.FuzzyDateTime(datetime(2020, 10, 12, tzinfo=UTC))

    @classmethod
    def create_including_keyword_in_title_or_content(cls, size, board, keyword):
        PostFactory.create_batch(size // 2, board=board, title='{} 제목'.format(keyword))
        PostFactory.create_batch(size // 2, board=board, content='{} 내용'.format(keyword))

    @classmethod
    def create_batch_with_comments(cls, size, board):
        for i in range(size):
            post = PostFactory.create(board=board.id)
            CommentFactory.create_batch(size=randint(0, 100), post=post.id)
