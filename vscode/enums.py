from enum import Enum, IntEnum

__all__ = ("ViewColumn", "ConfigType", "ProgressLocation")


class ViewColumn(IntEnum):
    """Represents where a view should be shown in the editor."""

    Beside = -2
    Active = -1
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9


class ConfigType(Enum):
    boolean = "boolean"
    integer = "number"
    string = "string"


class ProgressLocation(IntEnum):
    SourceControl = 1
    Window = 10
    Notification = 15
