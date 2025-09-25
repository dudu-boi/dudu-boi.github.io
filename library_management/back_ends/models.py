from dataclasses import dataclass
from typing import Optional

@dataclass
class LinkInfo:
    url: str
    ts_start: Optional[str] = None
    ts_end: Optional[str] = None
    video_id: Optional[str] = None

@dataclass
class DownloadReport:
    succeeded: list
    skipped: list
    failed: list
    non_youtube: list