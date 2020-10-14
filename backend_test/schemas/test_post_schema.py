from backend.schemas.post_schema import PostSchema
from backend.models.post import Post
from backend.models.comment import Comment
import pytest


@pytest.fixture
def posts():
    c = Comment(content="댓글입니다", writer="작성자1")
    c.pk = "5f85469378ebc3de6b8cf152"
    p = Post(title="제목", content="내용", writer="작성자", comments=[c])
    p.pk = "gf85469378ebc3de6b8cf152"

    return [p]


def test_dump_posts_with_comments(posts):
    schema = PostSchema(many=True)

    result = schema.dump(posts)

    assert result is not None
    assert result[0]['comments'][0]['_id'] is "5f85469378ebc3de6b8cf152"
