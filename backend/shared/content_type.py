from enum import Enum

from backend.shared.base_type import BaseType


class ContentType(BaseType):
    POST = 'post'
    COMMENT = 'comment'
    SUB_COMMENT = 'sub_comment'
