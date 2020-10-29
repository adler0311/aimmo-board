from mongoengine import Document, StringField


class Board(Document):
    title = StringField()

    # @queryset_manager
    # def exclude_post(self, queryset: QuerySet, board_id, post_id):
    #     b = queryset.filter(id=board_id).get()
    #     return queryset.filter(id=board_id).update_one(
    #         posts=list(filter(lambda p: p.id != ObjectId(post_id), b.posts)))
    #
    # @queryset_manager
    # def add_post(self, queryset: QuerySet, board_id, post: Post):
    #     b = queryset.filter(id=board_id).get()
    #     return queryset.filter(id=board_id).update_one(posts=[post] + b.posts)
