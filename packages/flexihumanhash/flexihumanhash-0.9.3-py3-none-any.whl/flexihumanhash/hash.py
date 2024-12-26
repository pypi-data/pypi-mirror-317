from __future__ import annotations

from jinja2 import Environment, BaseLoader
from typing import Any
import os
import hashlib
import math

from .dict import FlexiDict
from .rand import RandomSource


class FlexiHumanHash:
    def __init__(self, template: str) -> None:
        self.template_str = template
        self.jinja_env: Environment = Environment(loader=BaseLoader)  # type: ignore
        dicts = FlexiDict.get_registry()
        for dict_name in dicts.keys():
            self.jinja_env.globals[dict_name] = JinjaExpr(self, dict_name, dicts[dict_name])
        self.jinja_template = self.jinja_env.from_string(self.template_str)
        self.call_records: list[JinjaExpr] = []
        self.rndctx: RandomSource | None = None
        # XXX: when rndctx is None rendering the template has side-effects recording calls to calculate entropy
        self.jinja_template.render()
        entropy = 1
        num_bits = 0
        for r in self.call_records:
            entropy *= r.dict.size
            num_bits += required_bits(r.dict.size)
        self.entropy = entropy
        self.entropy_bits = num_bits
        self.required_bytes = required_bytes(self.entropy_bits)

    def hash(self, data: bytes | int | str, alg: str = "blake2b") -> HashResult:
        input = data
        if isinstance(data, int):
            sz = required_bytes(required_bits(data))
            sz = sz if sz > 4 else 4
            data = data.to_bytes(sz, byteorder="big")

        if isinstance(data, str):
            data = data.encode()

        match alg:
            case "blake2b":
                data = hashlib.blake2b(data, digest_size=self.required_bytes).digest()
                source = f"hash:{alg}:{self.required_bytes}"
            case "blake2s":
                data = hashlib.blake2s(data, digest_size=self.required_bytes).digest()
                source = f"hash:{alg}:{self.required_bytes}"
            case "shake128":
                data = hashlib.shake_128(data).digest(self.required_bytes)
                source = f"hash:{alg}:{self.required_bytes}"
            case "shake256":
                data = hashlib.shake_256(data).digest(self.required_bytes)
                source = f"hash:{alg}:{self.required_bytes}"
            case "md5":
                data = hashlib.md5(data).digest()
                source = f"hash:{alg}"
            case "sha1":
                data = hashlib.sha1(data).digest()
                source = f"hash:{alg}"
            case "sha224":
                data = hashlib.sha224(data).digest()
                source = f"hash:{alg}"
            case "sha256":
                data = hashlib.sha256(data).digest()
                source = f"hash:{alg}"
            case "sha384":
                data = hashlib.sha384(data).digest()
                source = f"hash:{alg}"
            case "sha512":
                data = hashlib.sha512(data).digest()
                source = f"hash:{alg}"
            case "sha3-224":
                data = hashlib.sha3_224(data).digest()
                source = f"hash:{alg}"
            case "sha3-256":
                data = hashlib.sha3_256(data).digest()
                source = f"hash:{alg}"
            case "sha3-384":
                data = hashlib.sha3_384(data).digest()
                source = f"hash:{alg}"
            case "sha3-512":
                data = hashlib.sha3_512(data).digest()
                source = f"hash:{alg}"
            case _:
                raise TypeError(f"unknown hash algorithm: {alg}")

        res = self.from_bytes(data)
        res.input_source = source
        res.input = input
        return res

    # def hash_str(self, data: str) -> HashResult:
    #     return HashResult("")

    # from_hexstr

    # def hash_int(self, data: int) -> HashResult:
    #     return HashResult("")

    # def from_uuid

    def rand(self) -> HashResult:
        data = os.urandom(self.required_bytes)

        ret = self.from_bytes(data)
        ret.input_source = "rand"
        return ret

    def from_bytes(self, data: bytes) -> HashResult:
        input_data = data
        if len(data) < self.required_bytes:
            need_bytes = self.required_bytes - len(data)
            data = data + os.urandom(need_bytes)

        self.rndctx = RandomSource(data)
        ret = self.jinja_template.render()
        self.rndctx = None

        return HashResult(
            hasher=self,
            result=ret,
            input_source="bytes",
            input=input_data,
            input_data=input_data,
            data=data,
            bits_provided=len(input_data) * 8,
            bits_used=self.entropy_bits,
            entropy=self.entropy,
        )


class HashResult:
    def __init__(
        self,
        *,
        hasher: FlexiHumanHash,
        result: str,
        input: Any,
        input_data: bytes,
        data: bytes,
        bits_provided: int,
        input_source: str,
        bits_used: int,
        entropy: int,
    ) -> None:
        self.result = result
        self.input = input
        self.input_data = input_data
        self.data = data
        self.input_source = input_source
        self.bits_provided = bits_provided
        self.bits_used = bits_used
        self.entropy = entropy
        self.hasher = hasher

    def __str__(self) -> str:
        return self.result


class JinjaExpr:
    def __init__(self, hasher: FlexiHumanHash, name: str, flexi_dict: FlexiDict) -> None:
        self.hasher = hasher
        self.name = name
        self.dict = flexi_dict
        self.args: tuple[Any, ...] | None = None
        self.kwargs: dict[str, Any] | None = None

    def __call__(self, *args: Any, **kwargs: dict[str, Any]) -> str:
        if self.hasher.rndctx is None:
            self.preprocess(args, kwargs)
            return ""

        return self.get_word()

    def __str__(self) -> str:
        if self.hasher.rndctx is None:
            self.preprocess()
            return ""

        return self.get_word()

    def get_word(self) -> str:
        r = self.hasher.rndctx
        d = self.dict
        assert r is not None
        idx = r.get_max(d.size)
        return d.get_entry(idx)

    def preprocess(
        self,
        args: tuple[Any, ...] = tuple(),
        kwargs: dict[str, Any] = dict(),
    ) -> None:
        self.args = args
        self.kwargs = kwargs
        self.hasher.call_records.append(self)
        self.dict = self.dict.preprocess(args, kwargs)


def required_bits(n: int) -> int:
    return math.ceil(math.log2(n))


def required_bytes(bits: int) -> int:
    return math.ceil(bits / 8)
