from flask_classful import FlaskView
from backend.models.post import Post
from backend.schemas.post_schema import PostSchema

import logging

posts_schema = PostSchema(many=True)


class PostsView(FlaskView):
    def index(self):
        try:
            objects = Post.objects()
            posts = [] if len(objects) == 0 else objects
            result = posts_schema.dump(posts)

            return {'posts': result}
        except Exception as e:
            logging.debug(e)
            return 'Internal Server Error', 500
