from mongoengine.queryset.manager import queryset_manager
from mongoengine.queryset.queryset import QuerySet, BaseQuerySet
from backend.models.content import Content
from mongoengine import StringField, ListField, ReferenceField
from mongoengine.base.fields import ObjectIdField
from backend.models.comment import Comment


class Post(Content):
    title = StringField()
    board_id = ObjectIdField('boardId')
    comments = ListField(ReferenceField(Comment))

    meta = {'indexes': [
        {'fields': ['$title', '$content']}
    ]}

    @queryset_manager
    def get_posts_with_parameters(doc_cls, queryset: QuerySet, order_type, limit, keyword):
        if order_type is None:
            order_type = 'created'
        if limit is None:
            limit = 10

        result: BaseQuerySet = queryset.order_by('-' + order_type)

        if keyword is not None:
            result = result.search_text(keyword)

        return result[:limit]
