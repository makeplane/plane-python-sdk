from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


# -------------------------- LITERALS --------------------------

TextDisplayFormat = Literal["single-line", "multi-line", "readonly"]
DateDisplayFormat = Literal["MMM dd, yyyy", "dd/MM/yyyy", "MM/dd/yyyy", "yyyy/MM/dd"]
NumberDisplayFormat = Literal["standard", "percentage", "currency"]
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


class StandardNumberAttributeSettings(BaseModel):
    """Settings for DECIMAL properties displayed as plain numbers, e.g. 1,234.50."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_format: Literal["standard"]
    decimal_places: int = Field(..., ge=0, le=4)
    thousand_separator: bool


class PercentageNumberAttributeSettings(BaseModel):
    """Settings for DECIMAL properties displayed as percentages, e.g. 12.5%."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_format: Literal["percentage"]
    decimal_places: int = Field(..., ge=0, le=4)


class CurrencyNumberAttributeSettings(BaseModel):
    """Settings for DECIMAL properties displayed as an amount of money, e.g. $1,234.50.

    Only the shape of `currency_code` is checked here; the server checks it against
    ISO 4217. Leave `decimal_places` unset to take the currency's own (2 for USD, 0
    for JPY) -- the server rejects a value that doesn't match the currency.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    display_format: Literal["currency"]
    currency_code: str = Field(..., pattern=r"^[A-Z]{3}$", description="ISO 4217, e.g. 'USD'")
    decimal_places: int | None = Field(None, ge=0, le=4)


# Settings for DECIMAL properties, picked by `display_format`
NumberAttributeSettings = Annotated[
    StandardNumberAttributeSettings
    | PercentageNumberAttributeSettings
    | CurrencyNumberAttributeSettings,
    Field(discriminator="display_format"),
]


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
