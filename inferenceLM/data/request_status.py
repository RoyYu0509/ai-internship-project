from enum import Enum

class RequestStatus(Enum):
    PENDING = 0
    WAITING = 1
    PREFILLING = 2
    DECODING = 3
    DONE = 4
