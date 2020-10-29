import factory
from factory import fuzzy

from backend.models.board import Board


class BoardFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Board

    title = fuzzy.FuzzyText(length=5)
