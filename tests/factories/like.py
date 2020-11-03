import factory
from factory import fuzzy

from backend.models.like import Like
from backend.shared.content_type import ContentType
from tests.factories.user import UserFactory


class LikeFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Like

    content_id = fuzzy.FuzzyText()
    content_type = fuzzy.FuzzyChoice(ContentType.list())
    user = factory.SubFactory(UserFactory)
    active = fuzzy.FuzzyChoice([True, False])

    @classmethod
    def create_batch_with_content_post(cls, size, **kwargs):
        result = []
        for _ in range(size):
            like = LikeFactory.create(content_type=ContentType.POST.value, **kwargs)
            result.append(like)
        return result

    @classmethod
    def create_like_with_post_list(cls, posts):
        likes = []
        for post in posts:
            like = cls.create(content_id=str(post.id), content_type='post')
            likes.append(like)
        return likes
