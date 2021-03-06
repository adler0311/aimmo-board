from backend.config import get_current_config
from backend.errors import ApiError
from backend.views.base import BaseView
from backend.models.like import Like
from backend.models.subcomment import SubComment
from typing import List
from backend.models.board import Board
from flask import Blueprint, Flask
from mongoengine import connect, DoesNotExist
from backend.models.post import Post
from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.models.comment import Comment
from lorem_text import lorem
from backend.views.posts import PostsView
from backend.views.comments import CommentsView
from backend.views.subcomments import SubCommentsView
from backend.views.users import UsersView
from backend.views.auth import AuthView
from backend.views.boards import BoardsView
from backend.views.likes import LikesView
import logging


def initiate_collection_for_test():
    Board.objects.delete()
    Post.objects.delete()
    Comment.objects.delete()
    User.objects.delete()
    AuthToken.objects.delete()
    SubComment.objects.delete()
    Like.objects.delete()

    title = "댓글 있는 글"
    content = lorem.paragraphs(1)
    writer = User(user_id='댓글 있는 글 작성자')
    writer.save()
    post_with_comment = Post(title=title, content=content, writer=writer)
    post_with_comment.save()

    comments = []
    for i in range(5):
        comment = lorem.words(3)
        writer = User(user_id='댓글 작성자 {}'.format(i + 1))
        writer.save()
        comments.append(Comment(content=comment,
                                writer=writer, post_id=post_with_comment.id))

    writer = User(
        user_id="대댓글 있는 댓글 작성자 1")
    writer.save()
    comment_with_sub_comments = Comment(content="대댓글 있는 댓글", writer=writer, post_id=post_with_comment.id)
    comment_with_sub_comments.save()
    sub_comments = []
    for i in range(3):
        writer = User(user_id='대댓글 작성자 {}'.format(i + 1))
        writer.save()
        sub_comment = SubComment(content="대댓글 {}".format(i + 1), writer=writer)
        sub_comment.save()
        sub_comments.append(sub_comment)

    Comment.objects(id=comment_with_sub_comments.id).update_one(subcomments=sub_comments)
    comments.append(comment_with_sub_comments)

    for comment in comments:
        comment.save()

    Post.objects(id=post_with_comment.id).update_one(comments=comments)

    posts: List[Post] = []
    for i in range(10):
        title = lorem.words(5)
        content = lorem.paragraphs(1)
        writer = User(user_id='글 작성자 {}'.format(i + 1))
        writer.save()

        post = Post(title=title, content=content, writer=writer)
        saved = post.save()
        posts.append(saved)

    # 검색할 글
    title = "검색글 제목"
    content = "검색 글 내용"
    writer = User(user_id='검색 글 작성자')
    writer.save()
    search_post = Post(title=title, content=content, writer=writer)
    saved_search_post = search_post.save()
    posts.append(saved_search_post)

    title = "공지 글"
    content = "공지 글 내용"
    writer = User(user_id='관리자')
    writer.save()

    search_post = Post(title=title, content=content, writer=writer, is_notice=True)
    saved_search_post = search_post.save()
    posts.append(saved_search_post)

    posts.append(post_with_comment)

    boards = [Board(title='게시판 {}'.format(i + 1)) for i in range(3)]
    Board.objects.insert(boards)

    board = Board(title='게시글 있는 게시판', posts=posts)
    saved_board = Board.save(board)
    for p in posts:
        p.update(board_id=saved_board.pk)

    post_with_comment.update(board_id=saved_board.pk)


def create_app():
    logging.basicConfig(level=logging.DEBUG)

    app = Flask(__name__)
    app.config.from_object(get_current_config())

    AuthView.register(app, route_base='/auth', base_class=BaseView, trailing_slash=False)
    UsersView.register(app, route_base='/users', base_class=BaseView, trailing_slash=False)

    BoardsView.register(app, route_base='/boards', base_class=BaseView, trailing_slash=False)
    PostsView.register(app, route_base='/boards/<string:board_id>/posts', base_class=BaseView, trailing_slash=False)
    CommentsView.register(app, route_base='/boards/<string:board_id>/posts/<string:post_id>/comments', base_class=BaseView, trailing_slash=False)
    SubCommentsView.register(app, route_base='/boards/<string:board_id>/posts/<string:post_id>/comments/<string:comment_id>/sub-comments', base_class=BaseView,
                             trailing_slash=False)

    LikesView.register(app, route_base='/likes', base_class=BaseView, trailing_slash=False)

    @app.errorhandler(DoesNotExist)
    def handle_document_does_not_exist(e):
        return 'Document Does not exist.', 404

    @app.errorhandler(ApiError)
    def handle_api_error(e: 'ApiError'):
        return e.message, e.status_code

    app.register_error_handler(404, handle_document_does_not_exist)
    app.register_error_handler(ApiError, handle_api_error)

    return app
