from __future__ import annotations
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Any

registry: dict[str, FlexiDict] = {}


class FlexiDict(ABC):
    @abstractmethod
    def get_entry(self, n: int) -> str: ...

    @abstractmethod
    def preprocess(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> FlexiDict: ...

    @property
    @abstractmethod
    def size(self) -> int: ...

    @staticmethod
    def register(name: str, d: FlexiDict) -> None:
        registry[name] = d

    @staticmethod
    def get_registry() -> dict[str, FlexiDict]:
        return registry


T = TypeVar("T", bound=type[FlexiDict])


def register_dict(name: str) -> Callable[[T], T]:
    def decorator(cls: T) -> T:
        FlexiDict.register(name, cls())
        return cls

    return decorator


class FlexiTextDict(FlexiDict):
    def __init__(self, name: str, words: list[str], min: int = 0, max: int = 2048) -> None:
        if min != 0 or max != 2048:
            self.words = [w for w in words if len(w) >= min and len(w) <= max]
        else:
            self.words = words
        self.sz = len(self.words)
        self.name = name

    def get_entry(self, n: int) -> str:
        return self.words[n]

    def preprocess(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> FlexiTextDict:
        return FlexiTextDict(self.name, self.words, *args, **kwargs)

    @property
    def size(self) -> int:
        return self.sz

    @staticmethod
    def from_file(name: str, path: Path) -> FlexiTextDict:
        fullpath = Path(path).resolve()
        with open(fullpath, "r") as file:
            lines = file.read().splitlines()
        d = FlexiTextDict(name, lines)
        FlexiDict.register(name, d)
        return d


@register_dict("hex")
class FlexiHexDict(FlexiDict):
    def __init__(self, size: int = 4) -> None:
        self.sz = size

    def get_entry(self, n: int) -> str:
        return f"{n:0{self.sz}x}"

    def preprocess(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> FlexiHexDict:
        return FlexiHexDict(*args, **kwargs)

    @property
    def size(self) -> int:
        num_bits = self.sz * 4
        ret: int = 2**num_bits
        return ret


@register_dict("decimal")
class FlexiDecimalDict(FlexiDict):
    def __init__(self, size: int = 4) -> None:
        self.sz = size

    def get_entry(self, n: int) -> str:
        return f"{n:0{self.sz}d}"

    @property
    def size(self) -> int:
        ret: int = 10**self.sz
        return ret

    def preprocess(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> FlexiDecimalDict:
        return FlexiDecimalDict(*args, **kwargs)


datadir = Path(__file__) / ".." / ".." / "data" / "build"
FlexiTextDict.from_file("noun", datadir / "noun")
FlexiTextDict.from_file("adj", datadir / "adjective")
FlexiTextDict.from_file("verb", datadir / "verb")
FlexiTextDict.from_file("city", datadir / "city")
FlexiTextDict.from_file("firstname", datadir / "first-name")
FlexiTextDict.from_file("lastname", datadir / "last-name")
FlexiTextDict.from_file("femalename", datadir / "female-name")
FlexiTextDict.from_file("malename", datadir / "male-name")
