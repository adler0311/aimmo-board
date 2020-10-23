from backend.views.base_view import BaseView
from flask import jsonify
from flask_classful import route
from backend.models.comment import Comment
from backend.models.post import Post
from backend.schemas.comment_schema import CommentSchema
from mongoengine import DoesNotExist, QuerySet
from bson import ObjectId
from backend.views.decorators import deserialize, input_data_required, token_required
from functools import wraps


comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()


def authorization_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        comment_id = kwargs['comment_id']
        auth_token = kwargs['auth_token']

        qs: QuerySet = Comment.objects
        comment = qs.get(pk=comment_id)

        if comment.writer.id != auth_token.user.id:
            return jsonify({'message': 'not authorized'}), 403

        return func(*args, **kwargs)

    return wrapper


class CommentsView(BaseView):
    route_base = '/posts/'

    @route('/<string:post_id>/comments/')
    def comments(self, post_id):
        comments = Comment.objects(post_id=post_id)
        result = comments_schema.dump(comments)
        return {'comments': result, 'postId': post_id}

    @token_required
    @input_data_required
    @deserialize(comment_schema)
    @route('/<post_id>/comments/', methods=['POST'])
    def post_comment(self, post_id, **kwargs):
        auth_token, data = kwargs['auth_token'], kwargs['data']

        try:
            p = Post.objects.get(id=post_id)

            c = Comment(**data, post_id=post_id, writer=auth_token.user)
            c.save()

            Post.objects(pk=p.id).update_one(comments=[c] + p.comments)
        except:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        return {'result': True}, 201

    @route('/<post_id>/comments/<comment_id>', methods=['GET'])
    def get(self, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
            result = comment_schema.dump(comment)
            return {'comment': result}, 200
        except DoesNotExist as e:
            return jsonify({'message': 'Post matching query does not exist'}), 404

    @token_required
    @authorization_required
    @input_data_required
    @deserialize(comment_schema)
    @route('/<string:post_id>/comments/<string:comment_id>', methods=['PUT'])
    def put_comment(self, post_id, comment_id, **kwargs):
        data = kwargs['data']

        result = Comment.objects(pk=comment_id).update_one(
            content=data['content'])

        if not result:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        return {'result': True}, 200

    @token_required
    @authorization_required
    @route('/<string:post_id>/comments/<string:comment_id>/', methods=['DELETE'])
    def delete(self, post_id, comment_id, **kwargs):

        result = Comment.objects(pk=comment_id).delete()

        if not result:
            return jsonify({'message': 'Comment matching id does not exist'}), 404

        try:
            p = Post.objects.get(pk=post_id)
            Post.objects(pk=p.id).update_one(comments=list(
                filter(lambda c: c.id != ObjectId(comment_id), p.comments)))
        except:
            return jsonify({'message': 'Post matching id does not exist'}), 404

        return {'result': True}, 200
