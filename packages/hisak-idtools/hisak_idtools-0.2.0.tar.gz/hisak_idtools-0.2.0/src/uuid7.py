import time
import uuid

_last_monotonicity_timestamp = 0
_time_ns = lambda: int(time.time() * 1000000000)
if hasattr(time, 'time_ns'):
    _time_ns = time.time_ns


class UUID(uuid.UUID):
    @property
    def time(self):
        # type: () -> int
        if self.version == 7:
            return int((self.int >> 80) / 1000)
        return super(UUID, self).time

    @property
    def time_ms(self):
        # type: () -> int
        return int(self.int >> 80)

    @property
    def time_ns(self):
        # type: () -> int
        return int(((self.int >> 80) * 1000000) + int((((self.int >> 64) & 0xfff) * 1000000) / 4096))

    @property
    def counter_seq(self):
        # type: () -> int
        return int((self.int >> 64) & 0xfff)


def _get_monotonicity_timestamp():
    # type: () -> (int, int)
    global _last_monotonicity_timestamp

    ns = _time_ns()
    ms, seq = divmod(ns, 1000000)
    ms &= 0xffffffffffff
    # RFC9562: Replace Leftmost Random Bits with Increased Clock Precision (Method 3)
    seq = int((float(seq) / 1000000) * 4096)
    ts = (ms << 12) + seq
    if ts <= _last_monotonicity_timestamp:
        ts = _last_monotonicity_timestamp + 1
        ms = (ts >> 12) & 0xffffffffffff
        seq = ts & 0xfff

    _last_monotonicity_timestamp = ts
    return ms, seq


def new_uuid7():
    # type: () -> UUID
    ms, seq = _get_monotonicity_timestamp()
    seq |= 0x7000
    return UUID(int=(((ms << 16) + seq) << 64) + (uuid.uuid4().int & 0xffffffffffffffff))
