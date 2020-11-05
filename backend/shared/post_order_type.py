from enum import Enum

from backend.shared.base_type import BaseType


class PostOrderType(BaseType):
    CREATED = 'created'
    COMMENT = 'comments'
    LIKE = 'likes'
