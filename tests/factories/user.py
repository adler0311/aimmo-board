import factory
from factory import fuzzy

from backend.models.user import User


class UserFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = User

    user_id = fuzzy.FuzzyText(length=6)
    password = fuzzy.FuzzyText(length=8)
