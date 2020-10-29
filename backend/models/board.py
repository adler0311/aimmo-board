from bson.objectid import ObjectId
from mongoengine.queryset.manager import queryset_manager
from mongoengine.queryset.queryset import QuerySet
from backend.models.post import Post
from mongoengine import Document, StringField

from mongoengine.fields import ListField, ReferenceField


class Board(Document):
    title = StringField()
    posts = ListField(ReferenceField(Post))

    @queryset_manager
    def exclude_post(self, queryset: QuerySet, board_id, post_id):
        b = queryset.filter(id=board_id).get()
        return queryset.filter(id=board_id).update_one(
            posts=list(filter(lambda p: p.id != ObjectId(post_id), b.posts)))

    @queryset_manager
    def add_post(self, queryset: QuerySet, board_id, post: Post):
        b = queryset.filter(id=board_id).get()
        return queryset.filter(id=board_id).update_one(posts=[post] + b.posts)
