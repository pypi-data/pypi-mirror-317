from typing import List, Optional

from _typeshed import Incomplete

class UefiBinary:
    KINDS: Incomplete
    guid: Incomplete
    def __init__(self, content: Optional[bytes], name: Optional[str], guid: str, ext: Optional[str]) -> None: ...
    @property
    def content(self) -> bytes: ...
    @property
    def name(self) -> str: ...
    @property
    def ext(self) -> str: ...
    @property
    def is_ok(self) -> bool: ...

class UefiExtractor:
    FILE_TYPES: Incomplete
    SECTION_TYPES: Incomplete
    UI: Incomplete
    binaries: Incomplete
    def __init__(self, firmware_data: bytes, file_guids: List[str]) -> None: ...
    def extract_all(self, ignore_guid: bool = ...) -> None: ...
