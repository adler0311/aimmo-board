from datetime import datetime, timedelta

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

    @classmethod
    def create_batch_in_created_desc(cls, size, **kwargs):
        now = datetime.now()

        comments = []
        for _ in range(size):
            comment = cls.create(created=now, parent=kwargs['parent_id'], writer=kwargs['writer'])
            comments.append(comment)
            now -= timedelta(minutes=1)
        return comments
