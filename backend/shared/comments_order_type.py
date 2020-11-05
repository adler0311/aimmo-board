from enum import Enum

from backend.shared.base_type import BaseType


class CommentsOrderType(BaseType):
    RECENT = 'recent'
    BEST = 'best'
