# Copyright (c) 2023 - 2024, HaiyangLi <quantocean.li at gmail dot com>
#
# SPDX-License-Identifier: Apache-2.0

from lionagi.libs.utils import is_same_dtype

from ..typing._pydantic import ConfigDict, Field, FieldInfo, field_validator
from ..typing._typing import UNDEFINED, Any, Callable, UndefinedType
from .schema_model import SchemaModel

__all__ = ("FieldModel",)


class FieldModel(SchemaModel):
    """Model for defining and managing field definitions.

    Provides a structured way to define fields with:
    - Type annotations and validation
    - Default values and factories
    - Documentation and metadata
    - Serialization options

    Example:
        ```python
        field = FieldModel(
            name="age",
            annotation=int,
            default=0,
            description="User age in years",
            validator=lambda v: v if v >= 0 else 0
        )
        ```

    Attributes:
        default: Default field value
        default_factory: Function to generate default value
        title: Field title for documentation
        description: Field description
        examples: Example values
        validators: Validation functions
        exclude: Exclude from serialization
        deprecated: Mark as deprecated
        frozen: Mark as immutable
        alias: Alternative field name
        alias_priority: Priority for alias resolution
        name: Field name (required)
        annotation: Type annotation
        validator: Validation function
        validator_kwargs: Validator parameters

    Notes:
        - All attributes except 'name' can be UNDEFINED
        - validator_kwargs are passed to field_validator decorator
        - Cannot have both default and default_factory
    """

    model_config = ConfigDict(
        extra="allow",
        validate_default=False,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    # Field configuration attributes
    default: Any = UNDEFINED  # Default value
    default_factory: Callable | UndefinedType = (
        UNDEFINED  # Factory function for default value
    )
    title: str | UndefinedType = UNDEFINED  # Field title
    description: str | UndefinedType = UNDEFINED  # Field description
    examples: list | UndefinedType = UNDEFINED  # Example values
    validators: list | UndefinedType = UNDEFINED  # Validation functions
    exclude: bool | UndefinedType = UNDEFINED  # Exclude from serialization
    deprecated: bool | UndefinedType = UNDEFINED  # Mark as deprecated
    frozen: bool | UndefinedType = UNDEFINED  # Mark as immutable
    alias: str | UndefinedType = UNDEFINED  # Alternative field name
    alias_priority: int | UndefinedType = (
        UNDEFINED  # Priority for alias resolution
    )

    # Core field attributes
    name: str | UndefinedType = Field(
        ..., exclude=True
    )  # Field name (required)
    annotation: type | Any = Field(UNDEFINED, exclude=True)  # Type annotation
    validator: Callable | Any = Field(
        UNDEFINED, exclude=True
    )  # Validation function
    validator_kwargs: dict | Any = Field(
        default_factory=dict, exclude=True
    )  # Validator parameters

    @field_validator("validators", mode="before")
    def _validate_validators(cls, v) -> list[Callable]:
        if v is None or v is UNDEFINED:
            return []
        if isinstance(v, Callable):
            return [v]
        if isinstance(v, list) and is_same_dtype(v, Callable):
            return v
        raise ValueError(
            "Validators must be a list of functions or a function"
        )

    @property
    def field_info(self) -> FieldInfo:
        """Generate Pydantic FieldInfo object from field configuration.

        Returns:
            FieldInfo object with all configured attributes

        Notes:
            - Uses clean dict to exclude UNDEFINED values
            - Sets annotation to Any if not specified
            - Preserves all metadata in field_info
        """
        annotation = (
            self.annotation if self.annotation is not UNDEFINED else Any
        )
        field_obj: FieldInfo = Field(**self.to_dict())  # type: ignore
        field_obj.annotation = annotation
        return field_obj

    @property
    def field_validator(self) -> dict[str, Callable] | None:
        """Generate field validator configuration.

        Returns:
            Dictionary mapping validator name to function,
            or None if no validator defined

        Notes:
            - Validator name is f"{field_name}_validator"
            - Uses validator_kwargs if provided
            - Returns None if validator is UNDEFINED
        """
        if self.validator is UNDEFINED:
            return None
        kwargs = self.validator_kwargs or {}
        return {
            f"{self.name}_validator": field_validator(self.name, **kwargs)(
                self.validator
            )
        }
