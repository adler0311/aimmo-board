from flask import request, jsonify
from flask_classful import FlaskView
from backend.models.post import Post
from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.schemas.post_schema import PostSchema
from mongoengine import DoesNotExist, QuerySet
from backend.views.decorators import token_required, input_data_required
from marshmallow import ValidationError
import logging

posts_schema = PostSchema(many=True)
post_schema = PostSchema()


def authorization_required(func):
    def wrapper(*args, **kwargs):
        id = kwargs['id']
        auth_token = kwargs['auth_token']

        qs: QuerySet = Post.objects
        post = qs.get(pk=id)

        if post.writer.id != auth_token.user.id:
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class PostsView(FlaskView):
    def index(self):
        try:
            posts = Post.objects()
            result = posts_schema.dump(posts)
            return {'posts': result}

        except Exception as e:
            logging.debug(e)
            return 'Internal Server Error', 500

    def get(self, id):
        try:
            post = Post.objects.get(pk=id)
            result = post_schema.dump(post)
            return {'data': result}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'Post matching query does not exist'}), 404

    @token_required
    @input_data_required
    def post(self, **kwargs):
        auth_token, json_data = kwargs['auth_token'], kwargs['json_data']

        try:
            data = post_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        data['writer'] = auth_token.user
        p = Post(**data)
        p.save()

        return {'result': True}, 201

    @token_required
    @authorization_required
    @input_data_required
    def put(self, id, **kwargs):
        auth_token, json_data = kwargs['auth_token'], kwargs['json_data']

        try:
            data = post_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        result = Post.objects(pk=id).update_one(
            title=data['title'], content=data['content'])

        if result is None:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    def delete(self, id, **kwargs):
        result = Post.objects(pk=id).delete()

        if not result:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200
