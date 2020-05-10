from enum import Enum
class GradingStatus(Enum):
    UNKNOWN = 0
    PENDING = 1
    SUCCESS = 2
    WRONG = 3
    TIME_LIMIT_EXCEEDED = 4
    MEMORY_LIMIT_EXCEEDED = 5
    COMPILE_ERROR = 6
    RUN_TIME_ERROR = 7

class ValidationMode(Enum):
    UNKNOWN = 0
    DEFAULT = 1
    EXACT = 2