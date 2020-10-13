from flask import Blueprint, Response
from backend.models.post import Post
from backend.schemas.post_schema import PostSchema
import json

blueprint = Blueprint('post', __name__)


posts_schema = PostSchema(many=True)


@blueprint.route('/posts', methods=['GET'])
def get_posts():
    objects = Post.objects()
    posts = [] if len(objects) == 0 else objects
    result = posts_schema.dump(posts)
    return {'posts': result}


@blueprint.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    NotImplemented


@blueprint.route('/post', methods=['POST'])
def add_post():
    NotImplemented


@blueprint.route('/post/<post_id>', methods=['PUT'])
def put_post(post_id):
    NotImplemented


@blueprint.route('/post/<post_id>', methods=['delete'])
def delete_post(post_id):
    NotImplemented
