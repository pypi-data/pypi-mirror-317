from typing import Iterator, Iterable
from enum import Enum
from dataclasses import dataclass

from ..run import Run
from ..types import ArgsDict


@dataclass
class BaseProvider:
    def __call__(self, run: Run, *, sweep=None, **_) -> Run:
        raise NotImplementedError

    def runs(self, config_keys: Iterable[str]) -> Iterator[ArgsDict]:
        raise NotImplementedError


@dataclass
class StatelessProvider(BaseProvider):
    class Env(str, Enum):
        ID = "RUN_ID"
        TAGS = "RUN_TAGS"

    def __call__(self, run: Run, *, sweep=None, **_) -> Run:
        if sweep:
            run.env[self.Env.TAGS.value] = ",".join(sweep.tags)

        run.env[self.Env.ID.value] = run.id

        return run

    def runs(self, _):
        return []
