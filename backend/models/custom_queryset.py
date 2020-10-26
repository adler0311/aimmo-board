from mongoengine import QuerySet


class AwesomeQuerySet(QuerySet):
    def remove_sub_content_ref(self):

        # Board.objects(id=b.id).update_one(posts=list(
        #     filter(lambda p: p.id != ObjectId(post_id), b.posts)))
        self.with_id('').update_one()
