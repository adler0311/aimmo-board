import factory
from factory import fuzzy
from backend.models.auth_token import AuthToken
from tests.factories.user import UserFactory


class AuthTokenFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = AuthToken

    token = fuzzy.FuzzyText(length=20)
    user = factory.SubFactory(UserFactory)

