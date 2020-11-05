from enum import Enum

from backend.shared.base_type import BaseType


class UserPostType(BaseType):
    WRITE = 'write'
    LIKE = 'like'
