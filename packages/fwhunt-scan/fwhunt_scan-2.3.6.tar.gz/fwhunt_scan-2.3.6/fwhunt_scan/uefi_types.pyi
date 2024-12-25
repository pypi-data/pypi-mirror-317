from enum import Enum
from typing import Optional

from _typeshed import Incomplete

class SmiKind(Enum):
    CHILD_SW_SMI: int
    SW_SMI: int
    USB_SMI: int
    SX_SMI: int
    IO_TRAP_SMI: int
    GPI_SMI: int
    TCO_SMI: int
    STANDBY_BUTTON_SMI: int
    PERIODIC_TIMER_SMI: int
    POWER_BUTTON_SMI: int
    ICHN_SMI: int
    PCH_TCO_SMI: int
    PCH_PCIE_SMI: int
    PCH_ACPI_SMI: int
    PCH_GPIO_UNLOCK_SMI: int
    PCH_SMI: int
    PCH_ESPI_SMI: int
    ACPI_EN_SMI: int
    ACPI_DIS_SMI: int

class UefiService:
    name: Incomplete
    address: Incomplete
    def __init__(self, name: str, address: int) -> None: ...
    @property
    def __dict__(self): ...

class UefiGuid:
    value: Incomplete
    name: Incomplete
    def __init__(self, value: str, name: str) -> None: ...
    @property
    def bytes(self) -> bytes: ...
    @property
    def __dict__(self): ...

class UefiProtocol(UefiGuid):
    address: Incomplete
    guid_address: Incomplete
    service: Incomplete
    def __init__(self, name: str, address: int, value: str, guid_address: int, service: str) -> None: ...
    @property
    def __dict__(self): ...

class UefiProtocolGuid(UefiGuid):
    address: Incomplete
    def __init__(self, name: str, address: int, value: str) -> None: ...
    @property
    def __dict__(self): ...

class NvramVariable:
    name: Incomplete
    guid: Incomplete
    service: Incomplete
    def __init__(self, name: str, guid: str, service: UefiService) -> None: ...
    @property
    def __dict__(self): ...

class SmiHandler:
    address: Incomplete
    kind: Incomplete
    def __init__(self, address: int, kind: SmiKind) -> None: ...
    @property
    def place(self): ...
    @property
    def __dict__(self): ...

class ChildSwSmiHandler(SmiHandler):
    handler_guid: Incomplete
    def __init__(self, handler_guid: Optional[str], address: int) -> None: ...
    @property
    def __dict__(self): ...
