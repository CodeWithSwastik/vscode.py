from typing import List, Union, Type
from vscode.enums import ConfigType


__all__ = ("EnumConfig", "Config")


class BaseConfig:
    def __init__(self, *, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, conf_dict):
        return cls(**conf_dict)

    def to_dict(self):
        return {"description": self.description}

    def __repr__(self):
        return f"<vscode.BaseConfig name={self.name} description={self.description}>"


class EnumConfig(BaseConfig):
    def __repr__(self):
        return f"<vscode.EnumConfig name={self.name} description={self.description}>"


class Config(BaseConfig):
    def __init__(
        self,
        name: str,
        description: str,
        input_type: Type[Union[str, int, bool]],
        enums: List[EnumConfig] = [],
        default=None,
    ) -> None:
        if input_type not in (bool, str, int):
            raise TypeError("input_type must be either the bool, str or int class")

        types = {
            bool: ConfigType.boolean,
            str: ConfigType.string,
            int: ConfigType.integer,
        }
        input_type = types[input_type]

        super().__init__(name=name, description=description)

        self.type = input_type.name
        self.default = default
        self.enums = enums

    def to_dict(self) -> dict:
        out = super().to_dict()

        out["type"] = self.type
        out["default"] = self.default

        if self.enums:
            out["enum"] = [enum.name for enum in self.enums]
            out["enumDescriptions"] = [enum.description for enum in self.enums]

        return out

    def __repr__(self):
        return f"<vscode.Config name={self.name} description={self.description} type={self.type} default={self.default} enums={[repr(enum) for enum in self.enums]}>"
