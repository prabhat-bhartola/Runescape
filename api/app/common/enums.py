from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def contains(cls, value):
        return any(member.value == value for member in cls)
