from mongoengine import Document, StringField
from mongoengine.queryset.manager import queryset_manager
from mongoengine.queryset.visitor import Q


class User(Document):
    user_id = StringField(required=True)
    password = StringField(required=True)

    @queryset_manager
    def get_user_by_id_and_password(self, queryset, user_id, password):
        return queryset.filter(Q(user_id=user_id) & Q(password=password)).first()
