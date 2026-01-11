from __future__ import annotations

import hashlib

_MAX_SIGNED_63 = (1 << 63) - 1

def stable_long_place_id(place_key: str) -> int:
    if not place_key:
        return 0

    h = hashlib.sha1(place_key.encode("utf-8")).hexdigest()
    v = int(h[:16], 16)
    v = v & _MAX_SIGNED_63
    return int(v)