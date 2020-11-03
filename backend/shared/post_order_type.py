from enum import Enum


class PostOrderType(Enum):
    CREATED = 'created'
    COMMENT = 'comments'
    LIKE = 'likes'

    @staticmethod
    def list():
        return list(map(lambda o: o.value, PostOrderType))
