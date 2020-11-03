from enum import Enum


class ContentType(Enum):
    POST = 'post'
    COMMENT = 'comment'
    SUB_COMMENT = 'sub_comment'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ContentType))
