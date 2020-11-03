from datetime import datetime

import factory
from dateutil.tz import UTC
from factory import fuzzy

from backend.models.comment import Comment


class CommentFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Comment

    content = fuzzy.FuzzyText(length=5)
    created = fuzzy.FuzzyDateTime(datetime(2020, 10, 12, tzinfo=UTC))
