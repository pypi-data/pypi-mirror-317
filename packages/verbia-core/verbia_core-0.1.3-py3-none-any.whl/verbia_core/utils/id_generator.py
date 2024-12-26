import random

from verbia_core.utils import time_provider


class SequenceIdGenerator:
    """
    64-bit ID generator
    """

    PARTITION_BITS = 7
    TIMESTAMP_BITS = 40
    DOMAIN_BITS = 4
    SEQUENCE_BITS = 12

    TIME_OFFSET = 1609971600000
    SEQUENCE_STEP = 17

    TIMESTAMP_MASK = (1 << TIMESTAMP_BITS) - 1
    SEQUENCE_MASK = (1 << SEQUENCE_BITS) - 1

    PARTITION_ID = 3
    DOMAIN_ID = 3
    last_timestamp = 0
    sequence = 0

    @classmethod
    def suid(cls):
        return str(cls.uid())

    @classmethod
    def uid(cls):
        timestamp = time_provider.time_mills_from_now()

        if timestamp == cls.last_timestamp:
            cls.sequence = (cls.sequence + cls.SEQUENCE_STEP) & cls.SEQUENCE_MASK
        else:
            cls.sequence = random.randint(0, (1 << cls.SEQUENCE_BITS) - 1)

        cls.last_timestamp = timestamp

        return (
            cls.PARTITION_ID
            << (cls.TIMESTAMP_BITS + cls.DOMAIN_BITS + cls.SEQUENCE_BITS)
            | ((timestamp - cls.TIME_OFFSET) & cls.TIMESTAMP_MASK)
            << (cls.DOMAIN_BITS + cls.SEQUENCE_BITS)
            | (cls.DOMAIN_ID << cls.SEQUENCE_BITS)
            | cls.sequence
        )
