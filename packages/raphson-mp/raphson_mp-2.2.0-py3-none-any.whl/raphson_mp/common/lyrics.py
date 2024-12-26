import re
from abc import ABC
from dataclasses import dataclass


class Lyrics(ABC):
    source: str


@dataclass
class LyricsLine:
    start_time: float
    text: str


@dataclass
class TimeSyncedLyrics(Lyrics):
    source: str
    text: list[LyricsLine]

    def to_plain(self) -> "PlainLyrics":
        text = "\n".join([line.text for line in self.text])
        return PlainLyrics(self.source, text)

    def to_lrc(self) -> str:
        lrc = ""
        for line in self.text:
            minutes, seconds = divmod(line.start_time, 60)
            lrc += f"[{int(minutes):02d}:{seconds:05.2f}] {line.text}\n"
        return lrc

    @classmethod
    def from_lrc(cls, source: str, lrc: str):
        lines: list[LyricsLine] = []
        for line in lrc.splitlines():
            matches = re.findall(r"\[(\d{2}):(\d{2})\.(\d{2})\](?: (.*))?", line)
            if matches:
                minutes, seconds, centiseconds, text = matches[0]
                lines.append(LyricsLine(int(minutes) * 60 + int(seconds) + int(centiseconds) / 100, text))
        return cls(source, lines)


@dataclass
class PlainLyrics(Lyrics):
    source: str
    text: str
