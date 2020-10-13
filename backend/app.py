import time
from flask import Flask
from mongoengine import connect
from backend.rest import post
from backend.models.post import Post
from lorem_text import lorem
from backend.views.quotes_view import QuotesView
from backend.views.posts_view import PostsView
import logging


def initiate_collection_for_test():
    Post.objects.delete()

    posts = []
    for i in range(10):
        title = lorem.sentence()
        content = lorem.paragraphs(1)
        writer = '작성자 {}'.format(i + 1)

        posts.append({'title': title, 'content': content, 'writer': writer})

    Post.objects.insert([Post(**data) for data in posts])


def create_app():
    logging.basicConfig(level=logging.DEBUG)

    connect('test')
    initiate_collection_for_test()

    app = Flask(__name__)

    PostsView.register(app)
    return app
