from datetime import datetime, timedelta

import factory
from dateutil.tz import UTC
from factory import fuzzy

from backend.models.comment import Comment


class CommentFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Comment

    content = fuzzy.FuzzyText(length=5)
    created = fuzzy.FuzzyDateTime(datetime(2020, 10, 12, tzinfo=UTC))
    likes = fuzzy.FuzzyInteger(low=0, high=1000)

    @classmethod
    def create_batch_in_created_desc(cls, size, **kwargs):
        now = datetime.now()

        comments = []
        for _ in range(size):
            comment = cls.create(created=now, post=kwargs['post_id'], writer=kwargs['writer'])
            comments.append(comment)
            now -= timedelta(minutes=1)
        return comments
