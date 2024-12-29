import sys
from abc import ABC, abstractmethod
from typing import List


class Stream(ABC):
    @abstractmethod
    def write(self, text: str) -> None:
        pass

    def close(self) -> None:
        pass


class FileOutputStream(Stream):
    def __init__(self, outfile: str):
        self.outfile = outfile

    def write(self, text: str) -> None:
        with open(self.outfile, "a") as f:
            f.write(text)


class ConsoleStream(Stream):
    def __init__(self):
        pass

    def write(self, text: str) -> None:
        sys.stdout.write(text)
        sys.stdout.flush()


class MultiStream(Stream):
    def __init__(self, streams: List[Stream]):
        self.streams = streams

    def write(self, text: str) -> None:
        for stream in self.streams:
            stream.write(text)

    def close(self) -> None:
        for stream in self.streams:
            stream.close()


class NullOutStream(Stream):
    def write(self, text: str) -> None:
        pass
