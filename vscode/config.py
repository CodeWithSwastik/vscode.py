from typing import List
from enum import Enum


__all__ = ("ConfigType", "EnumConfig", "Config")

class ConfigType(Enum):
    boolean = "boolean"
    integer = "number"
    string = "string"

class BaseConfig:
    def __init__(self, *, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, conf_dict):
        return cls(**conf_dict)

    def to_dict(self):
        return {"name": self.name, "description": self.description}

    def __repr__(self):
        return f"<vscode.BaseConfig name={self.name} description={self.description}>"

class EnumConfig(BaseConfig):
    def __repr__(self):
        return f"<vscode.EnumConfig name={self.name} description={self.description}>"

class Config(BaseConfig):
    def __init__(self, *, name: str, description: str, input_type, enums: List[BaseConfig] = [], default = None) -> None:
        if not isinstance(input_type, ConfigType):
            return

        super().__init__(name=name, description=description)

        self.type = input_type
        self.default = default
        self.enums = enums

    def to_dict(self) -> dict:
        out = super().to_dict()

        out["type"] = self.type
        out["default"] = self.default

        if len(self.enums):
            out["enum"] = [enum.name for enum in self.enums]
            out["enumDescriptions"] = [enum.description for enum in self.enums]

        return out
    
    def __repr__(self):
        return f"<vscode.Config name={self.name} description={self.description} type={self.type} default={self.default} enums={[repr(enum) for enum in self.enums]}>"