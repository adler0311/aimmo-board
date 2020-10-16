from flask import request, jsonify
from flask_classful import FlaskView
from backend.models.post import Post
from backend.models.auth_token import AuthToken
from backend.schemas.post_schema import PostSchema
from mongoengine import DoesNotExist

import logging

posts_schema = PostSchema(many=True)
post_schema = PostSchema()


class PostsView(FlaskView):
    def index(self):
        try:
            posts = Post.objects()
            result = posts_schema.dump(posts)
            return {'posts': result}

        except Exception as e:
            logging.debug(e)
            return 'Internal Server Error', 500

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        try:
            data = post_schema.load(json_data)
        except ValueError as err:
            return jsonify(err.messages), 422

        p = Post(**data)
        p.save()

        return {'result': True}, 201

    def get(self, id):
        try:
            post = Post.objects.get(pk=id)
            result = post_schema.dump(post)
            return {'data': result}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'Post matching query does not exist'}), 404

    def put(self, id):
        token = request.headers.get('Authorization')

        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        try:
            data = post_schema.load(json_data)
        except ValueError as err:
            return jsonify(err.messages), 422

        auth_token = AuthToken.objects.get(token=token)
        post = Post.objects.get(pk=id)

        if post.user.id != auth_token.user.id:
            return jsonify({'message': 'authentication required'}), 401

        result = Post.objects(pk=id).update_one(
            title=data['title'], content=data['content'])

        if result is None:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200

    def delete(self, id):
        result = Post.objects(pk=id).delete()

        if not result:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200
