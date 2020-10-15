from flask import request, jsonify
from flask_classful import FlaskView, route
from backend.models.comment import Comment
from backend.models.post import Post
from backend.schemas.comment_schema import CommentSchema
from mongoengine import DoesNotExist

import logging

comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()


class CommentsView(FlaskView):
    route_base = '/posts/'

    @route('/<string:post_id>/comments/')
    def comments(self, post_id):
        try:
            comments = Comment.objects(post_id=post_id)
            result = comments_schema.dump(comments)
            return {'comments': result, 'postId': post_id}

        except Exception as e:
            logging.debug(e)
            return 'Internal Server Error', 500

    @route('/<string:post_id>/comments/', methods=['POST'])
    def post_comment(self, post_id):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        try:
            data = comment_schema.load(json_data)
        except ValueError as err:
            return jsonify(err.messages), 400

        c = Comment(**data, post_id=post_id)
        c.save()

        p = Post.objects.get(id=post_id)
        Post.objects(pk=p.id).update_one(comments=[c] + p.comments)

        return {'result': True}, 201

    # def get(self, id):
    #     try:
    #         post = Post.objects.get(pk=id)
    #         result = post_schema.dump(post)
    #         return {'data': result}, 200
    #     except DoesNotExist as e:
    #         return jsonify({'message': 'Post matching query does not exist'}), 404

    # def put(self, id):
    #     json_data = request.get_json()
    #     if not json_data:
    #         return jsonify({'message': 'No input data provided'}), 400

    #     try:
    #         data = post_schema.load(json_data)
    #     except ValueError as err:
    #         return jsonify(err.messages), 422

    #     result = Post.objects(pk=id).update_one(
    #         title=data['title'], content=data['content'])

    #     if result is None:
    #         return jsonify({'message': 'Post matching id does not exist'}), 404

    #     return {'result': True}, 200

    # def delete(self, id):
    #     result = Post.objects(pk=id).delete()

    #     if not result:
    #         return jsonify({'message': 'Post matching id does not exist'}), 404

    #     return {'result': True}, 200
