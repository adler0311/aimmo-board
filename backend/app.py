import time
from flask import Flask
from mongoengine import connect
from backend.models.post import Post
from backend.models.comment import Comment
from lorem_text import lorem
from backend.views.posts_view import PostsView
from backend.views.comments_view import CommentsView
import logging


def initiate_collection_for_test():
    Post.objects.delete()

    comments = []
    for i in range(5):
        c_comment = lorem.words(3)
        writer = '댓글 작성자 {}'.format(i + 1)
        comments.append(Comment(content=c_comment, writer=writer))

    Comment.objects.insert(comments)

    posts = []
    for i in range(10):
        title = lorem.words(5)
        content = lorem.paragraphs(1)
        writer = '작성자 {}'.format(i + 1)

        posts.append({'title': title, 'content': content,
                      'writer': writer, 'comments': comments})

    Post.objects.insert([Post(**data) for data in posts])


def create_app():
    logging.basicConfig(level=logging.DEBUG)

    connect('test')
    initiate_collection_for_test()

    app = Flask(__name__)

    PostsView.register(app)
    # CommentsView.register(app, route_prefix='/posts/<p')
    return app
