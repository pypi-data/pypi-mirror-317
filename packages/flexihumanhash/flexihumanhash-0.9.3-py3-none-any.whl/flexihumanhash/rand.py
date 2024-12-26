from __future__ import annotations

import uuid

class RandomSource:
    def __init__(self, b: bytes) -> None:
        # print(f"creating random source with {len(b)} bytes")
        self.bytes = b
        self.big_num = int.from_bytes(self.bytes, byteorder="big")

    def get_max(self, max: int) -> int:
        # print(f"starting: {self.big_num}")
        self.big_num, res = divmod(self.big_num, max)
        # print(f"max: {max}, res: {res}, remaining: {self.big_num}")
        return res

    @staticmethod
    def from_uuid(u: uuid.UUID | str) -> RandomSource:
        if isinstance(u, str):
            u = uuid.UUID(u)
        return RandomSource(u.bytes)

    # from_hash(alg: str, alg_opts)
    # from_rand(nbytes: int = 16)
