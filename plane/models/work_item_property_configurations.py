from typing import Literal

from pydantic import BaseModel, ConfigDict


# -------------------------- LITERALS --------------------------

TextDisplayFormat = Literal["single-line", "multi-line", "readonly"]
DateDisplayFormat = Literal["MMM dd, yyyy", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy/MM/dd"]
DropdownAttributeKey = Literal["single_select", "multi_select"]
IconKey = Literal[
    "AlignLeft", "Hash", "CircleChevronDown", "ToggleLeft", "Calendar", "UsersRound", "Link2"
]
OperationMode = Literal["create", "update"]


# -------------------------- SETTINGS --------------------------


class TextAttributeSettings(BaseModel):
    """Settings for TEXT properties."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_format: TextDisplayFormat


class DateAttributeSettings(BaseModel):
    """Settings for DATETIME properties."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_format: DateDisplayFormat


# -------------------------- UI CONFIGURATIONS (optional helpers) --------------------------


class ConfigurationOption(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    labelKey: str
    value: str


class ConfigurationDetails(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    componentToRender: Literal["radio-input"]
    options: list[ConfigurationOption]
    verticalLayout: bool


class SettingsConfigurations(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    keyToUpdate: list[str]
    allowedEditingModes: list[OperationMode]
    configurations: ConfigurationDetails
