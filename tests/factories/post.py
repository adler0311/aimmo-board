import factory
from factory import fuzzy

from backend.models.board import Board
#
# type = StringField()
#     content = StringField()
#     writer = ReferenceField(User)
#     likes = IntField()
#     created = DateTimeField(default=datetime.datetime.now)
from backend.models.post import Post
from tests.factories.board import BoardFactory


class PostFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Post

    title = fuzzy.FuzzyText(length=5)
    board = factory.SubFactory(BoardFactory)
    likes = 10
    content = fuzzy.FuzzyText(length=20)
