from datetime import datetime

import factory
from dateutil.tz import UTC
from factory import fuzzy

from backend.models.subcomment import SubComment
from tests.factories.comment import CommentFactory
from tests.factories.post import PostFactory


class SubCommentFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = SubComment

    content = fuzzy.FuzzyText(length=5)
    created = fuzzy.FuzzyDateTime(datetime(2020, 10, 12, tzinfo=UTC))
    post = factory.SubFactory(PostFactory)
    parent = factory.SubFactory(CommentFactory)
