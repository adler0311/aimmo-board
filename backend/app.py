from backend.views.base_view import BaseView
from backend.models.like import Like
from backend.models.subcomment import Subcomment
from typing import List
from backend.models.board import Board
from flask import Flask
from mongoengine import connect
from backend.models.post import Post
from backend.models.user import User
from backend.models.auth_token import AuthToken
from backend.models.comment import Comment
from lorem_text import lorem
from backend.views.posts_view import PostsView
from backend.views.comments_view import CommentsView
from backend.views.users_view import UsersView
from backend.views.auth_view import AuthView
from backend.views.boards_view import BoardsView
from backend.views.subcomments_view import SubcommentsView
from backend.views.likes_view import LikesView
import logging


def initiate_collection_for_test():
    Board.objects.delete()
    Post.objects.delete()
    Comment.objects.delete()
    User.objects.delete()
    AuthToken.objects.delete()
    Subcomment.objects.delete()
    Like.objects.delete()

    title = "댓글 있는 글"
    content = lorem.paragraphs(1)
    writer = User(user_id='댓글 있는 글 작성자')
    writer.save()
    post_with_comment = Post(title=title, content=content, writer=writer)
    post_with_comment.save()

    comments = []
    for i in range(5):
        c_comment = lorem.words(3)
        writer = User(user_id='댓글 작성자 {}'.format(i+1))
        writer.save()
        comments.append(Comment(content=c_comment,
                                writer=writer, post_id=post_with_comment.id))

    writer = User(
        user_id="대댓글 있는 댓글 작성자 1")
    writer.save()
    c_with_sub = Comment(content="대댓글 있는 댓글", writer=writer,
                         post_id=post_with_comment.id)
    c_with_sub.save()
    subcomments = []
    for i in range(3):
        writer = User(user_id='대댓글 작성자 {}'.format(i+1))
        writer.save()
        sub = Subcomment(content="대댓글 {}".format(i+1), writer=writer)
        sub.save()
        subcomments.append(sub)

    Comment.objects(id=c_with_sub.id).update_one(subcomments=subcomments)
    comments.append(c_with_sub)

    for comment in comments:
        comment.save()

    Post.objects(id=post_with_comment.id).update_one(comments=comments)

    posts: List[Post] = []
    for i in range(10):
        title = lorem.words(5)
        content = lorem.paragraphs(1)
        writer = User(user_id='글 작성자 {}'.format(i + 1))
        writer.save()

        p = Post(title=title, content=content, writer=writer)
        saved = p.save()
        posts.append(saved)

    # 검색할 글
    title = "검색글 제목"
    content = "검색 글 내용"
    writer = User(user_id='검색 글 작성자')
    writer.save()
    search_p = Post(title=title, content=content, writer=writer)
    saved_search_p = search_p.save()
    posts.append(saved_search_p)

    posts.append(post_with_comment)

    boards = [Board(title='게시판 {}'.format(i+1)) for i in range(3)]
    Board.objects.insert(boards)

    board = Board(title='게시글 있는 게시판', posts=posts)
    saved_board = Board.save(board)
    for p in posts:
        p.update(board_id=saved_board.pk)

    post_with_comment.update(board_id=saved_board.pk)


def create_app():
    logging.basicConfig(level=logging.DEBUG)

    connect('test')
    initiate_collection_for_test()

    app = Flask(__name__)

    PostsView.register(app, base_class=BaseView)
    CommentsView.register(app, base_class=BaseView)
    UsersView.register(app, base_class=BaseView)
    AuthView.register(app, base_class=BaseView)
    BoardsView.register(app, base_class=BaseView)
    SubcommentsView.register(app, base_class=BaseView)
    LikesView.register(app, base_class=BaseView)

    return app
